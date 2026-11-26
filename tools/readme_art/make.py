"""Builds every README graphic in assets/readme/, in a light and a dark version.

    python3 tools/readme_art/make.py

Eval numbers are read from evals/real/results.json, so the graphics always match the eval.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from svgkit import Doc, icon  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
OUT = os.path.join(ROOT, "assets", "readme")
RES = json.load(open(os.path.join(ROOT, "evals", "real", "results.json")))

THEMES = {
    "light": dict(
        card="#ffffff", card2="#f6f8fa", line="#d8dee4", line2="#eaeef2", ink="#0b1220", ink2="#3d4756", mute="#6b7685",
        brand="#0d9488", brand2="#4f46e5", brandsoft="#e6f6f4", coral="#f43f5e", amberc="#f59e0b",
        green="#15803d", greensoft="#e7f6ec", amber="#b45309", ambersoft="#fdf3e1", red="#c81e3a", redsoft="#fde8ec",
        blue="#2563eb", bluesoft="#e8efff", grey="#94a3b8", greysoft="#f1f5f9",
        shadow="#1f2937", shadowop="0.07",
    ),
    "dark": dict(
        card="#111722", card2="#0d121b", line="#273142", line2="#1c2432", ink="#f2f5f9", ink2="#c3ccd8", mute="#8a96a8",
        brand="#2dd4bf", brand2="#8b8cff", brandsoft="#0e2b2a", coral="#ff6b81", amberc="#fbbf24",
        green="#4ade80", greensoft="#0f2a1b", amber="#fbbf24", ambersoft="#2e2410", red="#ff6b81", redsoft="#341620",
        blue="#7aa2ff", bluesoft="#16213d", grey="#64748b", greysoft="#18202d",
        shadow="#000000", shadowop="0.35",
    ),
}
BALLS = ["#f43f5e", "#f59e0b", "#14b8a6"]


def card(d, t, x, y, w, h, r=20, fill=None, stroke=None, shadow=True):
    if shadow:
        if not any('id="sh"' in s for s in d.defs):
            d.adddef(f'<filter id="sh" x="-10%" y="-10%" width="120%" height="140%"><feDropShadow dx="0" dy="6" stdDeviation="10" flood-color="{t["shadow"]}" flood-opacity="{t["shadowop"]}"/></filter>')
        d.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill or t["card"]}" stroke="{stroke or t["line"]}" filter="url(#sh)"/>')
    else:
        d.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill or t["card"]}" stroke="{stroke or t["line"]}"/>')


def grad(d, gid, c1, c2, x2=1, y2=0):
    d.adddef(f'<linearGradient id="{gid}" x1="0" y1="0" x2="{x2}" y2="{y2}"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>')


def eyebrow(d, t, x, y, label, anchor="start"):
    d.text(x, y, label.upper(), 15, t["brand"], 700, anchor=anchor, track=0.12)


def tick(d, cx, cy, col, r=11, fill=None, sw=2.2):
    d.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill or col}"/>')
    d.add(f'<path d="M{cx-5} {cy} l3.5 3.5 6.5-7" fill="none" stroke="{"#fff" if fill is None else col}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>')


def bubble(d, x, y, w, text, size, fill, ink, mine=True, stroke=None, dash=False, mono=False):
    h = size * 2.3
    st = f' stroke="{stroke}" stroke-width="1.5"' + (' stroke-dasharray="5 4"' if dash else "") if stroke else ""
    if mine:
        d.add(f'<path d="M{x+16} {y}H{x+w-16}Q{x+w} {y} {x+w} {y+16}V{y+h-6}Q{x+w} {y+h} {x+w-6} {y+h}H{x+16}Q{x} {y+h} {x} {y+h-16}V{y+16}Q{x} {y} {x+16} {y}Z" fill="{fill}"{st}/>')
    else:
        d.add(f'<path d="M{x+16} {y}H{x+w-16}Q{x+w} {y} {x+w} {y+16}V{y+h-16}Q{x+w} {y+h} {x+w-16} {y+h}H{x+6}Q{x} {y+h} {x} {y+h-6}V{y+16}Q{x} {y} {x+16} {y}Z" fill="{fill}"{st}/>')
    d.text(x + 16, y + h / 2 + size * 0.36, text, size, ink, 550, mono=mono)
    return h


# =====================================================================
def hero(mode):
    t = THEMES[mode]
    W, H = 1200, 580
    dark = mode == "dark"
    d = Doc(W, H, "Juggle: layer messages on your AI while it works. Nothing gets dropped. A free skill that keeps every request, applies your corrections and flags real clashes.")
    if dark:
        grad(d, "bg", "#06131a", "#111437", 1, 1)
        bgline = "#ffffff"
    else:
        grad(d, "bg", "#f4fbfa", "#eef0fb", 1, 1)
        bgline = "#0d9488"
    d.adddef(f'<clipPath id="clip"><rect width="{W}" height="{H}" rx="28"/></clipPath>')
    d.adddef(f'<radialGradient id="glow1" cx="0.82" cy="0.2" r="0.6"><stop offset="0" stop-color="{"#14b8a6" if dark else "#99f6e4"}" stop-opacity="{0.35 if dark else 0.6}"/><stop offset="1" stop-color="#14b8a6" stop-opacity="0"/></radialGradient>')
    d.adddef(f'<radialGradient id="glow2" cx="0.02" cy="1" r="0.6"><stop offset="0" stop-color="{"#6366f1" if dark else "#c7d2fe"}" stop-opacity="{0.35 if dark else 0.55}"/><stop offset="1" stop-color="#6366f1" stop-opacity="0"/></radialGradient>')
    d.adddef(f'<pattern id="dots" width="28" height="28" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.3" fill="{bgline}" fill-opacity="{0.07 if dark else 0.09}"/></pattern>')
    grad(d, "word", "#ffffff" if dark else "#0b1220", "#5eead4" if dark else "#0f766e")
    for i, c in enumerate(BALLS):
        d.adddef(f'<radialGradient id="ball{i}" cx="0.35" cy="0.3" r="0.75"><stop offset="0" stop-color="#ffffff" stop-opacity="0.65"/><stop offset="0.35" stop-color="{c}"/><stop offset="1" stop-color="{c}"/></radialGradient>')
    d.add('<g clip-path="url(#clip)">')
    d.add(f'<rect width="{W}" height="{H}" fill="url(#bg)"/><rect width="{W}" height="{H}" fill="url(#dots)"/>')
    d.add(f'<rect width="{W}" height="{H}" fill="url(#glow1)"/><rect width="{W}" height="{H}" fill="url(#glow2)"/>')
    # juggling arc behind the phone
    arc = "#ffffff" if dark else "#0f766e"
    d.add(f'<path d="M640 470 C 640 40, 1180 40, 1180 470" fill="none" stroke="{arc}" stroke-opacity="{0.16 if dark else 0.18}" stroke-width="2.5" stroke-dasharray="3 10" stroke-linecap="round"/>')
    for (cx, cy, r), i in zip([(676, 210, 22), (910, 66, 26), (1150, 236, 20)], range(3)):
        d.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#ball{i})"/>')
    d.add('</g>')
    d.add(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="28" fill="none" stroke="{"#ffffff" if dark else "#0d9488"}" stroke-opacity="{0.08 if dark else 0.14}"/>')

    ink = "#ffffff" if dark else t["ink"]
    ink2 = "#b9c6d6" if dark else t["ink2"]
    px, py = 64, 70
    label = "Agent skill  ·  v1.0.0  ·  Free and open source"
    w = d.measure(label, 16, 600) + 42
    d.add(f'<rect x="{px}" y="{py}" width="{w:.0f}" height="34" rx="17" fill="{"#ffffff" if dark else "#0d9488"}" fill-opacity="0.08" stroke="{"#ffffff" if dark else "#0d9488"}" stroke-opacity="{0.18 if dark else 0.28}"/>')
    d.add(f'<circle cx="{px+20}" cy="{py+17}" r="4" fill="{"#4ade80" if dark else "#16a34a"}"/>')
    d.text(px + 32, py + 23, label, 16, ink2 if dark else t["brand"], 600)
    d.text(60, 214, "Juggle", 112, "url(#word)", 800, track=-0.035)
    d.text(64, 278, "Layer messages on your AI.", 40, ink, 650, track=-0.015)
    d.text(64, 326, "Nothing gets dropped.", 40, "#ff7a85" if dark else "#e11d48", 650, track=-0.015)
    d.para(64, 376, "A free skill for Claude and other AI agents. Send or queue more while it works: every request is kept, corrections stick, and the original job still gets done.", 20, ink2, 560, 1.5)
    cx = 64
    for lab, ic in [("Every ask kept", "list"), ("Corrections stick", "edit"), ("Clashes flagged", "stop")]:
        tw = d.measure(lab, 16, 600)
        cw = tw + 54
        d.add(f'<rect x="{cx}" y="{H-104}" width="{cw:.0f}" height="42" rx="21" fill="#ffffff" fill-opacity="{0.07 if dark else 0.92}" stroke="{"#ffffff" if dark else "#99e3da"}" stroke-opacity="{0.16 if dark else 1}"/>')
        icon(d, ic, cx + 15, H - 93, 20, "#5eead4" if dark else t["brand"], 2)
        d.text(cx + 41, H - 77, lab, 16, ink, 600)
        cx += cw + 9

    # phone mock-up
    X, Y, PW, PH = 760, 96, 352, 452
    d.adddef('<filter id="hs" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="18" stdDeviation="22" flood-color="#0b1026" flood-opacity="0.35"/></filter>')
    pf = "#0e1522" if dark else "#ffffff"
    pl = "#273247" if dark else "#dfe5ee"
    d.add(f'<rect x="{X}" y="{Y}" width="{PW}" height="{PH}" rx="36" fill="{pf}" stroke="{pl}" stroke-width="1.5" filter="url(#hs)"/>')
    d.add(f'<rect x="{X+PW/2-44}" y="{Y+14}" width="88" height="22" rx="11" fill="{"#05080e" if dark else "#0b1220"}"/>')
    yy = Y + 58
    me = "#0d9488" if not dark else "#14b8a6"
    ai = "#18202e" if dark else "#f1f4f8"
    bubble(d, X + 96, yy, 238, "Email Printful: 200 tees", 14.5, me, "#ffffff")
    yy += 44
    bubble(d, X + 18, yy, 150, "Drafting it now…", 14.5, ai, ink2, mine=False)
    yy += 46
    d.text(X + PW - 20, yy + 4, "QUEUED WHILE IT WORKS", 11.5, t["mute"], 700, anchor="end", track=0.08)
    yy += 12
    bubble(d, X + 132, yy, 202, "wait its 500 not 200", 14.5, "none", ink, stroke=me, dash=True)
    yy += 42
    bubble(d, X + 106, yy, 228, "n sign it off as Hyder", 14.5, "none", ink, stroke=me, dash=True)
    yy += 52
    # reply card
    rf = "#122a2a" if dark else "#effaf8"
    d.add(f'<rect x="{X+18}" y="{yy}" width="{PW-36}" height="146" rx="16" fill="{rf}" stroke="{me}" stroke-opacity="0.45"/>')
    d.text(X + 34, yy + 28, "Changed to 500 and signed as Hyder.", 14.5, ink, 650)
    d.text(X + 34, yy + 50, "Here's the email: …", 14.5, ink2, 500)
    d.add(f'<path d="M{X+34} {yy+66}H{X+PW-34}" stroke="{me}" stroke-opacity="0.3"/>')
    rows = [("Done", "R1 email (500, Hyder)", t["green"]), ("Merged", "R2, R3 into R1", t["blue"]), ("Next", "nothing waiting", t["mute"])]
    ry = yy + 90
    for lab, txt, col in rows:
        d.add(f'<circle cx="{X+40}" cy="{ry-5}" r="4.5" fill="{col}"/>')
        d.text(X + 54, ry, lab, 13.5, col, 700, mono=True)
        d.text(X + 122, ry, txt, 13.5, ink2, 500, mono=True)
        ry += 22
    d.text(X + PW - 26, Y + PH - 16, "Illustration", 12, t["mute"], 500, anchor="end", opacity=0.8)
    return d


# =====================================================================
def specs(mode):
    t = THEMES[mode]
    W, H = 1200, 500
    h, dv = RES["heldout"], RES["dev"]
    SPECS = [
        (f"{h['juggle_pct']}%", "on held-out tests", f"vs {h['none_pct']}% with no skill. Never tuned on"),
        (f"{dv['juggle_pct']}%", "on development tests", f"vs {dv['none_pct']}% with no skill"),
        (f"{RES['layer_heldout']['juggle_pct']}%", "layering checks passed", f"Held-out. {RES['layer_heldout']['none_pct']}% with no skill"),
        ("9", "kinds of message sorted", "Addition, correction, stop, question and more"),
        (str(RES["scenarios"]), "real-life test chats", f"{RES['heldout_n']} held out, written before the skill"),
        (str(RES["tests"]), "automated tests", "Ledger script and skill text"),
        ("6", "places it works", "Claude, Codex, Cursor and any chat app"),
        ("£0", "free forever", "MIT licence. No installs, no sign-ups"),
    ]
    d = Doc(W, H, "Juggle at a glance: " + "; ".join(f"{a} {b} ({c})" for a, b, c in SPECS) + ".")
    card(d, t, 10, 10, W - 20, H - 30, 24)
    eyebrow(d, t, 50, 62, "At a glance")
    d.text(W - 50, 62, "Juggle 1.0", 17, t["mute"], 600, anchor="end", track=0.04)
    d.add(f'<path d="M10 86H{W-10}" stroke="{t["line2"]}"/>')
    cols, cw = 4, (W - 20) / 4
    for i, (big, lab, sub) in enumerate(SPECS):
        r, c = divmod(i, cols)
        x0 = 10 + c * cw
        y0 = 86 + r * 192
        if c:
            d.add(f'<path d="M{x0} {y0+28}V{y0+166}" stroke="{t["line2"]}"/>')
        if r and c == 0:
            d.add(f'<path d="M40 {y0}H{W-40}" stroke="{t["line2"]}"/>')
        gid = f"sg{i}"
        grad(d, gid, t["brand"], t["brand2"])
        d.text(x0 + 36, y0 + 82, big, 56, f"url(#{gid})" if i != 7 else t["ink"], 750, track=-0.03)
        d.text(x0 + 36, y0 + 116, lab, 20, t["ink"], 650)
        n = d.para(x0 + 36, y0 + 144, sub, 17, t["mute"], cw - 60, 1.4)
        assert n <= 2, sub
    return d


# =====================================================================
KINDS = [
    ("plus", "Addition", "also add navy", "Merged into the job now", "#0d9488"),
    ("edit", "Correction", "its 500 not 200", "Applied. Old value gone", "#2563eb"),
    ("swap", "Replacement", "make it a post instead", "Only the new version", "#7c3aed"),
    ("inbox", "New task", "btw what are the fees", "Kept separate, done after", "#0891b2"),
    ("question", "Question", "how long will this take", "Short answer, keeps going", "#ca8a04"),
    ("up", "Do this first", "faq first, its urgent", "Reordered. Nothing dropped", "#ea580c"),
    ("stop", "Stop", "nvm scrap that", "Stopped at once", "#e11d48"),
    ("repeat", "Sent twice", "check ebay  ·  check ebay", "Answered once", "#64748b"),
    ("ruler", "Standing rule", "never below £18", "Applies to everything", "#16a34a"),
]


def kinds(mode):
    t = THEMES[mode]
    W, H = 1200, 690
    d = Doc(W, H, "How it sorts each new message: " + "; ".join(f"{k} (for example '{e}'): {a}" for _, k, e, a, _ in KINDS) + ".")
    cols, gap = 3, 20
    cw = (W - 20 - gap * 2) / cols
    ch = 206
    for i, (ic, title, eg, act, col) in enumerate(KINDS):
        r, c = divmod(i, cols)
        x = 10 + c * (cw + gap)
        y = 10 + r * (ch + gap)
        card(d, t, x, y, cw, ch, 20)
        d.add(f'<rect x="{x+24}" y="{y+24}" width="46" height="46" rx="14" fill="{col}" fill-opacity="{0.12 if mode=="light" else 0.22}"/>')
        icon(d, ic, x + 35, y + 35, 24, col if mode == "light" else "#ffffff", 2)
        d.text(x + 86, y + 55, title, 23, t["ink"], 700, track=-0.01)
        d.add(f'<rect x="{x+24}" y="{y+90}" width="{cw-48}" height="40" rx="12" fill="{t["card2"]}" stroke="{t["line2"]}" stroke-dasharray="5 4"/>')
        assert d.measure(eg, 15.5, 500, mono=True) < cw - 80, eg
        d.text(x + 40, y + 115.5, eg, 15.5, t["ink2"], 500, mono=True)
        d.add(f'<path d="M{x+30} {y+162} h14 m-5 -5 l5 5 -5 5" fill="none" stroke="{col}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
        d.text(x + 56, y + 168, act, 18, t["ink"], 600)
    return d


# =====================================================================
FLOW = [
    ("inbox", "Arrives", "You send or queue more while it works."),
    ("layers", "Sort", "Each message gets one of 9 kinds."),
    ("anchor", "Rebuild", "One up-to-date brief. Newest wins."),
    ("check", "Deliver", "The finished work, urgent first."),
    ("list", "Check", "Done, next and needs you. Five lines max."),
]


def flow(mode):
    t = THEMES[mode]
    W, H = 1100, 440
    d = Doc(W, H, "How it works: a message arrives, it is sorted into one of 9 kinds, the whole conversation is rebuilt into one up-to-date brief, the finished work is delivered urgent first, then a short check lists what is done, next and needs you. A real clash, like a discount below your price floor, gets a safe default and a one-word override.")
    n = len(FLOW)
    gap = 18
    cw = (W - 20 - gap * (n - 1)) / n
    y, ch = 70, 236
    grad(d, "track", t["brand"], t["brand2"])
    d.add(f'<path d="M{10+cw/2} 40H{W-10-cw/2}" stroke="url(#track)" stroke-width="3" stroke-linecap="round"/>')
    for i, (ic, title, desc) in enumerate(FLOW):
        x = 10 + i * (cw + gap)
        cxm = x + cw / 2
        col = t["brand"] if i != 2 else t["brand2"]
        d.add(f'<circle cx="{cxm}" cy="40" r="17" fill="{t["card"]}" stroke="{col}" stroke-width="3"/>')
        d.text(cxm, 46.5, str(i + 1), 17, col, 750, anchor="middle")
        card(d, t, x, y, cw, ch, 20, stroke=col if i == 2 else None)
        d.add(f'<rect x="{x+24}" y="{y+26}" width="52" height="52" rx="15" fill="{col}" fill-opacity="{0.12 if mode=="light" else 0.2}"/>')
        icon(d, ic, x + 37, y + 39, 26, col, 2)
        d.text(x + 24, y + 120, title, 25, t["ink"], 700, track=-0.01)
        nl = d.para(x + 24, y + 154, desc, 18.5, t["ink2"], cw - 42, 1.42)
        assert nl <= 3, title
    lab = "Real clash? Safe version now, plus a one-word override. Never a silent guess."
    tw = d.measure(lab, 17, 600)
    bx = W / 2 - (tw + 44) / 2
    yb = y + ch + 50
    col = t["amber"]
    d.add(f'<path d="M{W/2} {y+ch+4}V{yb}" stroke="{col}" stroke-width="2.5" stroke-dasharray="6 6"/>')
    d.add(f'<rect x="{bx:.0f}" y="{yb}" width="{tw+44:.0f}" height="44" rx="22" fill="{t["ambersoft"]}" stroke="{col}" stroke-opacity="0.5"/>')
    icon(d, "stop", bx + 14, yb + 12, 20, col, 2)
    d.text(bx + 40, yb + 28, lab, 17, t["ink"], 600)
    return d


# =====================================================================
def anatomy(mode):
    """What a reply looks like, with labels."""
    t = THEMES[mode]
    W, H = 1200, 560
    d = Doc(W, H, "What a reply looks like. 1: one line up front showing it caught your new messages. 2: the finished work, urgent first, with quick answers on their own line. 3: a short check at the end, Done, Next and Needs you, five lines at most.")
    card(d, t, 10, 10, W - 20, H - 30, 24)
    eyebrow(d, t, 50, 62, "Anatomy of a reply")
    d.text(W - 50, 62, "After 3 layered messages", 17, t["mute"], 600, anchor="end")
    d.add(f'<path d="M10 86H{W-10}" stroke="{t["line2"]}"/>')
    # reply mock
    X, Y, RW = 50, 116, 640
    d.add(f'<rect x="{X}" y="{Y}" width="{RW}" height="390" rx="18" fill="{t["card2"]}" stroke="{t["line"]}"/>')
    blocks = [
        (Y + 22, 52, t["brand"], [("Changed the price to £24.99 and did the US page too.", 17.5, t["ink"], 700)]),
        (Y + 92, 176, t["blue"], [("UK shop: price is now £24.99.", 16.5, t["ink2"], 500),
                                   ("US shop: typo fixed (archieve to archive).", 16.5, t["ink2"], 500),
                                   ("US price: what should it be in dollars?", 16.5, t["ink2"], 500),
                                   ("I won't guess an exchange rate.", 16.5, t["ink2"], 500)]),
        (Y + 286, 86, t["green"], [("Done: R1 typo (UK, US). R2 price (UK)", 15.5, t["ink"], 500, True),
                                    ("Needs you: R3 US price in dollars", 15.5, t["ink"], 500, True)]),
    ]
    for by, bh, col, lines in blocks:
        d.add(f'<rect x="{X+16}" y="{by}" width="{RW-32}" height="{bh}" rx="12" fill="{col}" fill-opacity="{0.07 if mode=="light" else 0.12}" stroke="{col}" stroke-opacity="0.35"/>')
        d.add(f'<rect x="{X+16}" y="{by}" width="5" height="{bh}" rx="2.5" fill="{col}"/>')
        ly = by + 32
        for ln in lines:
            txt, sz, c, wg = ln[:4]
            mono = len(ln) > 4
            d.text(X + 40, ly, txt, sz, c, wg, mono=mono)
            ly += sz * 1.75
    notes = [
        (Y + 48, t["brand"], "1  One line up front", "Shows it caught your new messages, so you can tell at a glance."),
        (Y + 180, t["blue"], "2  The finished work", "Urgent first. Quick answers get their own line. Never 'let me finish'."),
        (Y + 330, t["green"], "3  A short check", "Done, Next, Needs you. Only when you asked for two or more things."),
    ]
    for ny, col, title, sub in notes:
        d.add(f'<path d="M{X+RW+4} {ny}H{X+RW+44}" stroke="{col}" stroke-width="2"/><circle cx="{X+RW+4}" cy="{ny}" r="4" fill="{col}"/>')
        d.text(X + RW + 60, ny + 6, title, 21, t["ink"], 700)
        d.para(X + RW + 60, ny + 36, sub, 17, t["ink2"], 400, 1.4)
    return d


# =====================================================================
def results(mode):
    t = THEMES[mode]
    W, H = 1200, 500
    rows = [("Held-out tests", RES["heldout"]), ("Development tests", RES["dev"]),
            ("Layering checks, held-out", RES["layer_heldout"]), ("Layering checks, development", RES["layer_dev"])]
    d = Doc(W, H, "Eval results on a small open model, gpt-oss-20b: " + "; ".join(f"{n}: {r['juggle_pct']}% with Juggle vs {r['none_pct']}% with no skill" for n, r in rows) + ".")
    card(d, t, 10, 10, W - 20, H - 30, 24)
    eyebrow(d, t, 50, 62, "Tested, not guessed")
    d.text(W - 50, 62, f"gpt-oss-20b  ·  blind judge  ·  {RES['date']}", 16, t["mute"], 600, anchor="end")
    d.add(f'<path d="M10 86H{W-10}" stroke="{t["line2"]}"/>')
    x0, bw = 470, 560
    grad(d, "bj", t["brand"], t["brand2"])
    y = 132
    for name, r in rows:
        d.text(50, y + 26, name, 19, t["ink"], 650)
        for k, (cond, fill, lab) in enumerate([("none", t["grey"], "No skill"), ("juggle", "url(#bj)", "Juggle")]):
            v = r[f"{cond}_pct"]
            by = y + k * 30
            d.add(f'<rect x="{x0}" y="{by}" width="{bw}" height="22" rx="11" fill="{t["greysoft"]}"/>')
            d.add(f'<rect x="{x0}" y="{by}" width="{bw*v/100:.1f}" height="22" rx="11" fill="{fill}"/>')
            d.text(x0 - 14, by + 16, lab, 14, t["mute"], 600, anchor="end")
            d.text(x0 + bw + 14, by + 17, f"{v}%", 18, t["ink"] if cond == "juggle" else t["mute"], 750 if cond == "juggle" else 550)
        y += 78
    d.text(50, H - 44, "Same model, same chats, with and without the skill. Graded blind: the judge never sees which is which.", 15.5, t["mute"], 500)
    return d


# =====================================================================
COMPARE = [
    ("Answers your whole request, not just the last message", "Left to chance", "Rebuilds the brief"),
    ("Corrections replace the old value everywhere", "Left to chance", "Newest wins"),
    ("'Do this first' without dropping the rest", "Left to chance", "Reorders, drops nothing"),
    ("Stops when you say stop", "Usually", "Cancels that item"),
    ("Spots a new message breaking your own rule", "Left to chance", "Safe default, you override"),
    ("Reads fast phone typing without fuss", "Usually", "Reads for intent"),
    ("Tells you what is done, next and waiting on you", "If you ask", "Every multi-ask reply"),
    ("Never claims it checked what it cannot check", "Left to chance", "Says how to check"),
]


def compare(mode):
    t = THEMES[mode]
    W = 1200
    rh, top = 60, 112
    H = top + rh * len(COMPARE) + 40
    d = Doc(W, H, "Your AI on its own versus with Juggle: " + "; ".join(f"{a}: {b} on its own, {c} with Juggle" for a, b, c in COMPARE) + ".")
    card(d, t, 10, 10, W - 20, H - 30, 24)
    c1, c2, c3 = 50, 650, 860
    d.add(f'<rect x="{c3-30}" y="26" width="{W-10-16-(c3-30)}" height="{H-62}" rx="16" fill="{t["brandsoft"]}"/>')
    d.text(c1, 74, "WHAT YOU GET", 15, t["mute"], 700, track=0.08)
    d.text(c2, 74, "YOUR AI ON ITS OWN", 15, t["mute"], 700, track=0.08)
    d.text(c3, 74, "WITH JUGGLE", 15, t["brand"], 750, track=0.08)
    d.add(f'<path d="M40 {top-12}H{W-40}" stroke="{t["line"]}"/>')
    for i, (feat, alone, jg) in enumerate(COMPARE):
        y = top + i * rh + 37
        assert d.measure(feat, 20, 600) < c2 - c1 - 30, feat
        d.text(c1, y, feat, 20, t["ink"], 600)
        d.add(f'<circle cx="{c2+6}" cy="{y-6}" r="6" fill="none" stroke="{t["mute"]}" stroke-width="2"/>')
        d.text(c2 + 24, y, alone, 18.5, t["mute"], 500)
        tick(d, c3 + 10, y - 6, t["brand"])
        d.text(c3 + 32, y, jg, 18.5, t["ink"], 650)
        if i < len(COMPARE) - 1:
            d.add(f'<path d="M40 {top+(i+1)*rh}H{c3-40}" stroke="{t["line2"]}"/>')
    return d


# =====================================================================
STATS = [
    ("-39%", "average drop in quality when a request arrives over several messages", "Laban et al., ICLR 2026"),
    ("95%", "of single-message quality kept when the pieces are joined into one brief first", "Same study. Juggle's core habit"),
    ("2x", "as unreliable: the same model swings far more between good and bad answers", "Same study, 15 models"),
]


def stats(mode):
    t = THEMES[mode]
    W, H = 1200, 290
    d = Doc(W, H, "The research behind it: " + "; ".join(f"{a} {b} ({c})" for a, b, c in STATS) + ".")
    gap = 20
    cw = (W - 20 - 2 * gap) / 3
    for i, (big, lab, src) in enumerate(STATS):
        x = 10 + i * (cw + gap)
        card(d, t, x, 10, cw, H - 30, 20)
        d.text(x + 30, 92, big, 50, t["coral"] if i != 1 else t["brand"], 750, track=-0.03)
        n = d.para(x + 30, 134, lab, 19, t["ink"], cw - 60, 1.4, 600)
        assert n <= 3, lab
        d.text(x + 30, H - 48, src, 16, t["mute"], 500)
    return d


# =====================================================================
def footer(mode):
    W, H = 1200, 220
    d = Doc(W, H, "Juggle. Free and open source under the MIT licence. Made by Hyder.")
    grad(d, "fb", "#061a1c", "#151447", 1, 1)
    d.adddef(f'<clipPath id="fc"><rect width="{W}" height="{H}" rx="24"/></clipPath>')
    for i, c in enumerate(BALLS):
        d.adddef(f'<radialGradient id="ball{i}" cx="0.35" cy="0.3" r="0.75"><stop offset="0" stop-color="#ffffff" stop-opacity="0.65"/><stop offset="0.35" stop-color="{c}"/><stop offset="1" stop-color="{c}"/></radialGradient>')
    d.add(f'<g clip-path="url(#fc)"><rect width="{W}" height="{H}" fill="url(#fb)"/>')
    d.add('<path d="M900 250 C 900 -30, 1180 -30, 1180 250" fill="none" stroke="#ffffff" stroke-opacity="0.15" stroke-width="2.5" stroke-dasharray="3 10" stroke-linecap="round"/></g>')
    for (cx, cy, r), i in zip([(928, 120, 18), (1040, 46, 22), (1150, 130, 16)], range(3)):
        d.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#ball{i})"/>')
    for i, (cx, cy) in enumerate([(84, 86), (118, 66), (150, 96)]):
        d.add(f'<circle cx="{cx}" cy="{cy}" r="14" fill="url(#ball{i})"/>')
    d.text(186, 112, "Juggle", 44, "#ffffff", 800, track=-0.03)
    d.text(188, 146, "Free and open source. MIT licence. Made by Hyder.", 19, "#b9c6d6", 500)
    d.text(188, 176, "Layer messages on your AI. Nothing gets dropped.", 17, "#8a9ab0", 500)
    return d


BADGES = [
    ("claude-code", "CLAUDE CODE", "term", "#d9774b", "#b8532a"),
    ("agents", "CODEX  ·  CURSOR  ·  AGENTS", "term", "#0d9488", "#4f46e5"),
    ("claude-ai", "CLAUDE.AI", "chat", "#c26a43", "#9a4a28"),
    ("chat-apps", "CHATGPT  ·  GEMINI  ·  ANY CHAT", "chat", "#2563eb", "#7c3aed"),
]


def badge(slug, label, ic, c1, c2):
    tw = Doc(10, 10, "").measure(label, 14, 700, track=0.08)
    W, H = int(tw + 62), 34
    d = Doc(W, H, label.title())
    grad(d, "bg", c1, c2)
    d.add(f'<rect width="{W}" height="{H}" rx="17" fill="url(#bg)"/>')
    icon(d, ic, 14, 8, 18, "#ffffff", 2)
    d.text(42, 22, label, 14, "#ffffff", 700, track=0.08)
    return d


ALL = dict(hero=hero, specs=specs, kinds=kinds, flow=flow, anatomy=anatomy, results=results, compare=compare, stats=stats, footer=footer)

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, fn in ALL.items():
        for mode in ("light", "dark"):
            if name == "footer" and mode == "dark":
                continue
            svg = fn(mode).render()
            p = os.path.join(OUT, f"{name}-{mode}.svg" if name != "footer" else "footer.svg")
            open(p, "w").write(svg)
            print(f"{os.path.relpath(p, ROOT)}  {len(svg)//1024} KB")
    for b in BADGES:
        open(os.path.join(OUT, f"badge-{b[0]}.svg"), "w").write(badge(*b).render())
