# Real-model evaluation

This folder holds a real-model test of Juggle: real replies from a real language model, graded
blind, with and without the skill.

## How it works

- **Model:** `gpt-oss-20b`, through the free anonymous Pollinations endpoint (no key, no cost).
  This is a small open model. It is not Claude, so absolute scores say little about how Juggle
  behaves in Claude.
- **Scenarios:** 30 conversations (`scenarios.json`, built by `make_scenarios.py`). Each one is a
  first request, the assistant starting on it, then one to four layered messages: corrections,
  additions, a replacement, a new unrelated task, a question, a change of priority, a stop, a
  clash with an earlier rule, typo-heavy phone messages, and the same message sent twice. The
  model writes its next reply.
  - `L01` to `L20`: a **development set**, used while writing the skill. Scores on it are optimistic.
  - `H01` to `H10`: a **held-out set**. It was written and committed (commit `8528332`, the first
    commit in this repo) **before the first line of SKILL.md**, run only once, on the final
    version, and never used for tuning. `tests/test_skill_text.py` fails if any of its distinctive
    wording appears in SKILL.md, AGENTS.md or the chat paste-in.
- **Checks:** each scenario has 3 to 5 specific checks plus 4 layering checks used everywhere:
  the original request is delivered, every later message is acted on or acknowledged, the newest
  wish wins or a real clash is flagged, and the reply is easy to read on a phone.
- **Conditions:** `none` is a plain "You are a helpful AI assistant." system prompt. Every other
  condition adds a skill text to it. Only the text is given; the model cannot open the reference
  files or run the ledger script.
- **Grading:** the same model acts as judge, twice per reply with different seeds. It sees the
  conversation, the checks and the reply, never the condition (ids are hashes; the key is in
  `judged/key.json`). The two judging rounds agreed on 94% of individual checks.

## Results (23 Nov 2026)

Final skill: `skill-versions/j5.md`, identical to `skills/juggle/SKILL.md` at release.
3 replies per scenario per condition, each judged twice.

| Set | No skill | Juggle | Chat paste-in only |
| --- | --- | --- | --- |
| **Held-out** (H01 to H10, 480 checks each) | 366 (76%) | **446 (93%)** | 453 (94%) |
| Layering checks only, held-out | 78% | **95%** | 96% |
| Development (L01 to L20, 972 checks each) | 747 (77%) | **890 (92%)** | not run |
| Layering checks only, development | 82% | **95%** | not run |

- **Held-out:** Juggle beat no skill on 6 scenarios, lost on 2 (H02 and H09, each by a few checks;
  for example one reply said "6 pm, then 7 pm" instead of replacing the time) and tied on 2. Average gain per scenario
  17 points, 95% bootstrap interval 4 to 30 points.
- **The 1,078-character chat paste-in** (for ChatGPT and other chat apps) did as well as the full
  skill on the held-out set. The full skill adds the ledger file for coding agents, examples and
  more detailed rules that a stronger model can use.
- **Weakest area:** clashes with an earlier rule (H04: a new message asks to say "100% organic
  cotton" after a rule not to mention cotton). No skill: the model refused outright in all three
  tries (17%). Juggle: 67%. One try handled it well, two still wrote "organic" claims.
- **Where no skill already does well:** simple corrections (H02, H09) and plain additions (H01,
  H05). Juggle mostly helps when a later message would otherwise swallow the original (H07, H10),
  when a question or new task arrives mid-job (H03, H08) and with rule clashes (H04).

### Development rounds

Each round changed SKILL.md and was scored on the development set only. Versions are in
`skill-versions/` (j1 was not saved separately; j2 is j1 plus the changes listed).

| Round | Change | Dev score (2 replies) |
| --- | --- | --- |
| j1 | First draft: ledger, nine kinds, protect the original, clashes, typos, reply shape | 87% (no skill 79%) |
| j2 | "Every reply carries the finished work"; never claim you checked; do the safe version, then ask | 93% |
| j3 | Small queued items done now; flag names that match two things; no invented business facts | 89% |
| j4 | Five checks before sending | 90% |
| j5 | Five core rules moved to the top | 92% with 3 replies (j2: 93% with 3 replies) |

j2 and j5 tied on the development set (within noise). j5 was chosen before the held-out run
because its extra rules target honesty failures seen in the replies (invented exchange rates,
claims of checks that never happened, invented product facts).

## Honest limits

- Small numbers: 10 held-out scenarios and 3 replies each. The gap is clear but the exact
  percentages will move between runs.
- The judge is the same small model, and it is lenient on honesty checks (it passed some replies
  that claimed an eBay name check the model cannot do). Grading is blind, so this applies to
  every condition equally.
- One reply out of 270 (`runs/none/H10_0.json`) failed repeatedly at the endpoint with seed 101
  and was regenerated with seed 131. The file records this.
- One-turn simulation: the model sees the queued messages as later user messages and answers
  once. A real multi-turn test in Claude Code, with tools and the ledger file, would be more
  informative and needs a signed-in Claude account.

## Re-running

```bash
python3 harness.py gen --cond none --samples 3 --only H
python3 harness.py gen --cond j5 --skill skill-versions/j5.md --samples 3 --only H
python3 harness.py judge --conds none,j5 --only H --rounds 2
python3 harness.py report --conds none,j5 --only H
```

The free endpoint changes over time, so new runs will not match these numbers exactly.
