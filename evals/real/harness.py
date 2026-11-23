#!/usr/bin/env python3
"""Real-model evaluation for Juggle, using a free anonymous model endpoint (no key, no cost).

Generate:  python3 harness.py gen --cond none|juggle --skill path/to/SKILL.md --samples 2 [--only L]
Judge:     python3 harness.py judge --conds none,juggle --rounds 2 [--only L]
Report:    python3 harness.py report --conds none,juggle [--only H]

Each scenario is a conversation: a first request, the assistant starting on it, then one or more
extra messages layered on top (corrections, additions, questions, a stop, a change of priority).
The model writes its next reply. L01 to L20 are a development set used while tuning the skill.
H01 to H10 are a held-out set, written before the first SKILL.md draft and never used for tuning.

Judging is blind: each reply gets a hashed id; the judge sees the conversation, the checks and the
reply, never the condition. The id-to-condition key is kept in judged/key.json.
"""
import argparse, json, os, random, time, urllib.request, urllib.error, hashlib, concurrent.futures as cf

HERE = os.path.dirname(os.path.abspath(__file__))
ENDPOINT = "https://text.pollinations.ai/openai"
MODEL = "openai-fast"  # served as gpt-oss-20b
GLOBAL = [
    "Delivers what the person first asked for (or what it became after their own corrections); it is not dropped or forgotten",
    "Every later message is acted on or clearly acknowledged; none is silently ignored",
    "Where a later message changed or clashed with an earlier one, the reply follows the newest wish, or flags a real clash instead of guessing",
    "Easy to read on a phone: clear, no padding, not a wall of text",
]
BASE_SYS = "You are a helpful AI assistant."


def ask(messages, retries=6, seed=7):
    body = json.dumps({"model": MODEL, "messages": messages, "private": True, "seed": seed}).encode()
    err = "empty reply"
    for attempt in range(retries):
        try:
            req = urllib.request.Request(ENDPOINT, data=body, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=300) as r:
                d = json.load(r)
            text = d["choices"][0]["message"]["content"]
            if text and text.strip():
                return text, d.get("model")
        except (urllib.error.URLError, TimeoutError, KeyError, json.JSONDecodeError, ConnectionError, OSError) as e:
            err = e
        time.sleep(5 * (attempt + 1))
    raise RuntimeError(f"failed after retries: {err}")


def scenarios(prefix=None):
    with open(os.path.join(HERE, "scenarios.json"), encoding="utf-8") as fh:
        return [s for s in json.load(fh) if not prefix or s["id"].startswith(prefix)]


def system_prompt(skill):
    system = BASE_SYS
    if skill:
        with open(skill, encoding="utf-8") as fh:
            system += ("\n\nThe following skill is installed and active. Follow it.\n\n<skill name=\"juggle\">\n"
                       + fh.read() + "\n</skill>")
    return system


def build_messages(s, system):
    msgs = [{"role": "system", "content": system}]
    for i, (role, text) in enumerate(s["turns"]):
        if i == 0:
            text = f"[Setting: {s['context']}]\n\n{text}"
        msgs.append({"role": role, "content": text})
    return msgs


def transcript(s):
    who = {"user": "PERSON", "assistant": "ASSISTANT"}
    return "\n".join(f"{who[r]}: {t}" for r, t in s["turns"])


def gen(cond, skill, samples, workers, prefix=None, tag=None):
    out = os.path.join(HERE, "runs", tag or cond)
    os.makedirs(out, exist_ok=True)
    system = system_prompt(skill)
    jobs = [(s, k, os.path.join(out, f"{s['id']}_{k}.json")) for s in scenarios(prefix) for k in range(samples)]
    jobs = [j for j in jobs if not os.path.exists(j[2])]

    def run(job):
        s, k, path = job
        text, model = ask(build_messages(s, system), seed=101 + k)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump({"id": s["id"], "sample": k, "cond": tag or cond, "model": model, "response": text}, fh, indent=1)
        return s["id"], k

    with cf.ThreadPoolExecutor(workers) as ex:
        for f in cf.as_completed([ex.submit(run, j) for j in jobs]):
            try:
                print("done", *f.result(), flush=True)
            except Exception as e:
                print("ERROR", e, flush=True)


JUDGE_SYS = ("You are a strict, fair examiner. A busy person sent an AI assistant a request, then layered "
             "extra messages on top while it was working. Grade the assistant's NEXT reply. "
             "For each numbered check, decide if the reply clearly meets it (1) or not (0). "
             "Judge only what the reply says. Partial or vague counts as 0. "
             "Answer with JSON only: {\"scores\": [0 or 1, ...], \"notes\": \"one short sentence\"}.")


def judge_prompt(s, response):
    checks = s["checks"] + GLOBAL
    return checks, (f"Setting: {s['context']}\n\nConversation so far:\n{transcript(s)}\n\n"
                    f"The assistant's next reply, to grade:\n<<<\n{response}\n>>>\n\nChecks:\n"
                    + "\n".join(f"{i+1}. {c}" for i, c in enumerate(checks))
                    + f"\n\nReturn exactly {len(checks)} scores in order.")


def judge(conds, workers, rounds, prefix=None):
    jdir = os.path.join(HERE, "judged")
    os.makedirs(jdir, exist_ok=True)
    keypath = os.path.join(jdir, "key.json")
    key = json.load(open(keypath)) if os.path.exists(keypath) else {}
    scen = {s["id"]: s for s in scenarios()}
    items = []
    for cond in conds:
        d = os.path.join(HERE, "runs", cond)
        for name in sorted(os.listdir(d)):
            if prefix and not name.startswith(prefix):
                continue
            rec = json.load(open(os.path.join(d, name)))
            bid = hashlib.sha256(f"{cond}/{name}/juggle".encode()).hexdigest()[:10]
            key[bid] = {"cond": cond, "id": rec["id"], "sample": rec["sample"]}
            for r in range(rounds):
                path = os.path.join(jdir, f"{bid}_{r}.json")
                if not os.path.exists(path):
                    items.append((bid, r, rec, path))
    json.dump(key, open(keypath, "w"), indent=1)
    random.Random(42).shuffle(items)

    def run(item):
        bid, r, rec, path = item
        checks, prompt = judge_prompt(scen[rec["id"]], rec["response"])
        for attempt in range(4):
            text, _ = ask([{"role": "system", "content": JUDGE_SYS}, {"role": "user", "content": prompt}], seed=500 + 10 * r + attempt)
            try:
                d = json.loads(text[text.index("{"): text.rindex("}") + 1])
                sc = [1 if int(x) else 0 for x in d["scores"]]
                if len(sc) == len(checks):
                    json.dump({"bid": bid, "round": r, "scores": sc, "notes": d.get("notes", "")}, open(path, "w"))
                    return bid, r
            except (ValueError, KeyError, TypeError):
                pass
        raise RuntimeError("judge gave bad JSON for " + bid)

    with cf.ThreadPoolExecutor(workers) as ex:
        for f in cf.as_completed([ex.submit(run, i) for i in items]):
            try:
                print("judged", *f.result(), flush=True)
            except Exception as e:
                print("ERROR", e, flush=True)


def tally(conds, prefix=None):
    jdir = os.path.join(HERE, "judged")
    key = json.load(open(os.path.join(jdir, "key.json")))
    scen = {s["id"]: s for s in scenarios()}
    tot = {c: [0, 0] for c in conds}
    glob = {c: [0, 0] for c in conds}
    per = {}
    for name in os.listdir(jdir):
        if name == "key.json":
            continue
        d = json.load(open(os.path.join(jdir, name)))
        k = key[d["bid"]]
        if k["cond"] not in tot or (prefix and not k["id"].startswith(prefix)):
            continue
        n_spec = len(scen[k["id"]]["checks"])
        tot[k["cond"]][0] += sum(d["scores"]); tot[k["cond"]][1] += len(d["scores"])
        glob[k["cond"]][0] += sum(d["scores"][n_spec:]); glob[k["cond"]][1] += len(d["scores"][n_spec:])
        p = per.setdefault(k["id"], {c: [0, 0] for c in conds})
        p[k["cond"]][0] += sum(d["scores"]); p[k["cond"]][1] += len(d["scores"])
    return tot, glob, per


def report(conds, prefix=None):
    tot, glob, per = tally(conds, prefix)
    pct = lambda a: f"{a[0]}/{a[1]} ({100*a[0]/a[1]:.0f}%)" if a[1] else "n/a"
    lines = ["| Scenario | " + " | ".join(conds) + " |", "|---|" + "---|" * len(conds)]
    for sid in sorted(per):
        lines.append(f"| {sid} | " + " | ".join(pct(per[sid][c]) for c in conds) + " |")
    lines.append("| **All checks** | " + " | ".join(f"**{pct(tot[c])}**" for c in conds) + " |")
    lines.append("| Layering checks only | " + " | ".join(pct(glob[c]) for c in conds) + " |")
    print("\n".join(lines))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["gen", "judge", "report"])
    ap.add_argument("--cond")
    ap.add_argument("--conds")
    ap.add_argument("--skill")
    ap.add_argument("--samples", type=int, default=2)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--rounds", type=int, default=2)
    ap.add_argument("--only", help="scenario ids starting with this, for example L (development) or H (held-out)")
    a = ap.parse_args()
    if a.cmd == "gen":
        gen(a.cond, a.skill, a.samples, a.workers, a.only)
    elif a.cmd == "judge":
        judge(a.conds.split(","), a.workers, a.rounds, a.only)
    else:
        report(a.conds.split(","), a.only)
