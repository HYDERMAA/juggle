#!/usr/bin/env python3
"""Juggle ledger: a tiny, plain-Markdown list of every request in a conversation.

Keeps the list in .juggle/ledger.md (or the path in JUGGLE_LEDGER, or --file) so it survives long
runs, compaction and new sessions. Standard library only.

    ledger.py add "Add dark mode toggle" --kind original      -> R1
    ledger.py add "Save button broken on mobile" --kind task  -> R2 (status next)
    ledger.py add "Do not touch the header" --kind rule       -> R3 (status active)
    ledger.py set R1 doing
    ledger.py set R2 done --note "fixed flex wrap in SaveBar.jsx"
    ledger.py show                 # whole table
    ledger.py open                 # only what is still open
    ledger.py check                # exit 1 if anything is still doing or next
    ledger.py clear --yes          # start a fresh ledger (old one kept as ledger-<n>.md)
"""
import argparse
import os
import re
import sys

KINDS = ["original", "addition", "correction", "replacement", "task", "question", "priority", "stop", "rule"]
STATUSES = ["doing", "next", "done", "changed", "cancelled", "needs-you", "active"]
OPEN = {"doing", "next"}
HEADER = ("# Juggle ledger\n\n"
          "Every request in this conversation, in the order it arrived. Nothing leaves this list\n"
          "except as done, changed or cancelled. Rules stay active until the person changes them.\n\n"
          "| # | Request | Kind | Status | Note |\n|---|---|---|---|---|\n")
ROW = re.compile(r"^\|\s*(R\d+)\s*\|(.*)\|\s*([a-z]+)\s*\|\s*([a-z-]+)\s*\|(.*)\|\s*$")


def default_path():
    return os.environ.get("JUGGLE_LEDGER") or os.path.join(os.getcwd(), ".juggle", "ledger.md")


def _esc(s):
    return " ".join(s.replace("|", "/").split())


def load(path):
    items = []
    if not os.path.exists(path):
        return items
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            m = ROW.match(line.rstrip("\n"))
            if m:
                items.append({"id": m.group(1), "text": m.group(2).strip(), "kind": m.group(3),
                              "status": m.group(4), "note": m.group(5).strip()})
    return items


def save(path, items):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    body = "".join(f"| {i['id']} | {_esc(i['text'])} | {i['kind']} | {i['status']} | {_esc(i['note'])} |\n" for i in items)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        fh.write(HEADER + body)
    os.replace(tmp, path)


def _norm(s):
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def add(items, text, kind="task", status=None):
    """Adds a request and returns (item, is_new). A repeat of an open request returns the old one."""
    if kind not in KINDS:
        raise ValueError(f"kind must be one of {', '.join(KINDS)}")
    text = _esc(text)
    if not text:
        raise ValueError("empty request")
    for it in items:
        if _norm(it["text"]) == _norm(text) and it["status"] in OPEN | {"active", "needs-you"}:
            return it, False
    if status is None:
        if kind == "rule":
            status = "active"
        elif kind == "original" or not any(i["status"] == "doing" for i in items):
            status = "doing"
        else:
            status = "next"
    if status not in STATUSES:
        raise ValueError(f"status must be one of {', '.join(STATUSES)}")
    n = max([int(i["id"][1:]) for i in items] or [0]) + 1
    it = {"id": f"R{n}", "text": text, "kind": kind, "status": status, "note": ""}
    items.append(it)
    return it, True


def set_status(items, rid, status, note=None):
    if status not in STATUSES:
        raise ValueError(f"status must be one of {', '.join(STATUSES)}")
    rid = rid.upper()
    for it in items:
        if it["id"] == rid:
            it["status"] = status
            if note is not None:
                it["note"] = _esc(note)
            return it
    raise KeyError(f"no request {rid}")


def open_items(items):
    return [i for i in items if i["status"] in OPEN]


def summary(items):
    """Short end-of-turn ledger check, as the skill asks for."""
    groups = [("Done", "done"), ("Doing", "doing"), ("Next", "next"), ("Needs you", "needs-you"),
              ("Changed", "changed"), ("Cancelled", "cancelled"), ("Rules", "active")]
    out = []
    for label, st in groups:
        hits = [f"{i['id']} {i['text']}" + (f" ({i['note']})" if i["note"] else "") for i in items if i["status"] == st]
        if hits:
            out.append(f"{label}: " + "; ".join(hits))
    return "\n".join(out) or "Ledger is empty."


def main(argv=None):
    ap = argparse.ArgumentParser(description="Juggle ledger: keep every layered request.")
    ap.add_argument("--file", default=None, help="ledger path (default .juggle/ledger.md or $JUGGLE_LEDGER)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add"); a.add_argument("text"); a.add_argument("--kind", default="task", choices=KINDS)
    a.add_argument("--status", choices=STATUSES)
    s = sub.add_parser("set"); s.add_argument("id"); s.add_argument("status", choices=STATUSES); s.add_argument("--note")
    sub.add_parser("show"); sub.add_parser("open"); sub.add_parser("check"); sub.add_parser("summary")
    c = sub.add_parser("clear"); c.add_argument("--yes", action="store_true")
    args = ap.parse_args(argv)
    path = args.file or default_path()
    items = load(path)

    if args.cmd == "add":
        it, new = add(items, args.text, args.kind, args.status)
        save(path, items)
        print(f"{it['id']} {'added' if new else 'already in the ledger'} ({it['status']})")
    elif args.cmd == "set":
        try:
            it = set_status(items, args.id, args.status, args.note)
        except KeyError as e:
            print(str(e).strip("'"), file=sys.stderr)
            return 2
        save(path, items)
        print(f"{it['id']} -> {it['status']}")
    elif args.cmd == "show":
        if not os.path.exists(path):
            print("No ledger yet.")
        else:
            with open(path, encoding="utf-8") as fh:
                print(fh.read(), end="")
    elif args.cmd == "open":
        for it in open_items(items) + [i for i in items if i["status"] == "needs-you"]:
            print(f"{it['id']} [{it['status']}] {it['text']}")
    elif args.cmd == "summary":
        print(summary(items))
    elif args.cmd == "check":
        left = open_items(items)
        waiting = [i for i in items if i["status"] == "needs-you"]
        for it in waiting:
            print(f"needs you: {it['id']} {it['text']}")
        if left:
            for it in left:
                print(f"still open: {it['id']} [{it['status']}] {it['text']}")
            print("Not finished: deliver these, or mark them done, cancelled or needs-you, and say so in your reply.")
            return 1
        print("All requests handled." if items else "Ledger is empty.")
    elif args.cmd == "clear":
        if not args.yes:
            print("Refusing to clear without --yes.", file=sys.stderr)
            return 2
        if os.path.exists(path):
            n = 1
            while os.path.exists(path[:-3] + f"-{n}.md"):
                n += 1
            os.replace(path, path[:-3] + f"-{n}.md")
            print(f"Old ledger kept as {os.path.basename(path)[:-3]}-{n}.md")
        save(path, [])
    return 0


if __name__ == "__main__":
    sys.exit(main())
