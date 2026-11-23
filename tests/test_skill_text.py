"""Guards the skill text: house style, size limits, the behaviours the eval relies on, no leaks
of the held-out scenarios into anything the model reads, and the release zip."""
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(ROOT, "skills", "juggle")


def read(*parts):
    with open(os.path.join(*parts), encoding="utf-8") as fh:
        return fh.read()


# behaviour -> phrases that must appear in SKILL.md (lower case)
SKILL_MUST = {
    "rebuild the brief": ["rebuild the brief", "newest wish winning"],
    "ledger and statuses": ["ledger", "doing", "next", "changed", "cancelled", "needs you"],
    "message kinds": ["addition", "correction", "replacement", "new task", "question", "priority change", "stop", "repeat", "rule"],
    "protect the original": ["protect the original", "keep good work already shown"],
    "clashes": ["ask only when", "safe default", "one word"],
    "typos": ["read for intent", "never comment on spelling"],
    "quality": ["every reply carries the finished work", "never claim", "finish the current step cleanly"],
    "reply shape": ["bluf", "done:", "next:", "needs you:"],
    "file ledger": ["scripts/ledger.py", ".juggle/ledger.md", "ledger.py check"],
}
AGENTS_MUST = ["rebuild the brief", "ledger", "newest wins", "stop", "safe version", "never comment on spelling",
               "every reply carries the finished work"]


def heldout_phrases():
    """Distinctive words from the held-out scenarios that must not appear in the skill text."""
    return ["lisbon", "vegetarian", "whatsapp", "the crown", "organic cotton", "cotton", "back10", "latvia",
            "newsletter", "side hustle", "market stall", "spanish", "promoted listing", "competitor",
            "test_checkout_total", "thursday"]


class SkillText(unittest.TestCase):
    def test_frontmatter(self):
        text = read(SKILL, "SKILL.md")
        self.assertTrue(text.startswith("---\nname: juggle\n"))
        desc = re.search(r"^description: (.*)$", text, re.M).group(1)
        self.assertLessEqual(len(desc), 200)
        self.assertNotIn("<", desc)
        self.assertLess(text.count("\n"), 500)

    def test_house_style(self):
        for rel in ("skills/juggle/SKILL.md", "skills/juggle/references/examples.md", "AGENTS.md",
                    "paste-into-chat.md", "README.md", "evals/real/README.md"):
            if not os.path.exists(os.path.join(ROOT, rel)):
                continue
            text = read(ROOT, rel)
            self.assertNotIn("\u2014", text, f"{rel}: no em dashes")
            for us in ("color ", "behavior", "summarize", "prioritize", "organize"):
                self.assertNotIn(us, text.lower(), f"{rel}: British spelling ({us})")

    def test_skill_covers_behaviours(self):
        text = read(SKILL, "SKILL.md").lower()
        for name, phrases in SKILL_MUST.items():
            for p in phrases:
                self.assertIn(p, text, f"{name}: missing '{p}'")

    def test_agents_and_cursor_rule(self):
        subprocess.run([sys.executable, os.path.join(ROOT, "tools", "build.py")], check=True, capture_output=True)
        for rel in ("AGENTS.md", os.path.join(".cursor", "rules", "juggle.mdc")):
            text = read(ROOT, rel).lower()
            for p in AGENTS_MUST:
                self.assertIn(p, text, f"{rel}: missing '{p}'")

    def test_paste_block_fits_chatgpt(self):
        block = re.search(r"```\n(.*?)```", read(ROOT, "paste-into-chat.md"), re.S).group(1)
        self.assertLessEqual(len(block), 1500)
        for p in ("newest wins", "stop", "done / next / needs you"):
            self.assertIn(p, block.lower())

    def test_no_heldout_leak(self):
        """The held-out set only means something if the skill was never shown it."""
        for rel in ("skills/juggle/SKILL.md", "AGENTS.md", "paste-into-chat.md"):
            text = read(ROOT, rel).lower()
            for p in heldout_phrases():
                self.assertNotIn(p, text, f"{rel} mentions held-out phrase '{p}'")

    def test_scenarios_well_formed(self):
        sc = json.loads(read(ROOT, "evals", "real", "scenarios.json"))
        ids = [s["id"] for s in sc]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(sum(i.startswith("H") for i in ids), 10)
        for s in sc:
            self.assertEqual(s["turns"][0][0], "user")
            self.assertEqual(s["turns"][-1][0], "user", s["id"])
            self.assertGreaterEqual(sum(r == "user" for r, _ in s["turns"]), 2, s["id"])
            self.assertTrue(3 <= len(s["checks"]) <= 5, s["id"])

    def test_zip_and_links(self):
        subprocess.run([sys.executable, os.path.join(ROOT, "tools", "build.py")], check=True, capture_output=True)
        with tempfile.TemporaryDirectory() as tmp:
            with zipfile.ZipFile(os.path.join(ROOT, "dist", "juggle.zip")) as z:
                z.extractall(tmp)
            base = os.path.join(tmp, "juggle")
            for must in ("SKILL.md", "LICENSE.txt", "scripts/ledger.py", "references/examples.md", "agents/openai.yaml"):
                self.assertTrue(os.path.exists(os.path.join(base, must)), must)
            for dirpath, _, files in os.walk(base):
                for f in files:
                    if f.endswith(".md"):
                        for target in re.findall(r"\]\(([^)\s]+)\)", read(dirpath, f)):
                            if target.startswith(("http", "#", "mailto:")):
                                continue
                            full = os.path.normpath(os.path.join(dirpath, target.split("#")[0]))
                            self.assertTrue(os.path.exists(full), f"{f} -> {target}")

    def test_readme_images_exist(self):
        if not os.path.exists(os.path.join(ROOT, "README.md")):
            self.skipTest("no README yet")
        for target in re.findall(r'(?:src|srcset)="([^"]+)"', read(ROOT, "README.md")):
            if not target.startswith("http"):
                self.assertTrue(os.path.exists(os.path.join(ROOT, target)), target)

    def test_no_secret_like_strings(self):
        pat = re.compile(r"(sk_(live|test)_[A-Za-z0-9]{8,}|sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{20,}|xox[bp]-[A-Za-z0-9-]{10,})")
        out = subprocess.run(["git", "ls-files", "-co", "--exclude-standard"], cwd=ROOT, capture_output=True, text=True).stdout.split()
        for rel in out:
            p = os.path.join(ROOT, rel)
            if not os.path.isfile(p) or rel.endswith((".png", ".zip")):
                continue
            with open(p, encoding="utf-8", errors="ignore") as fh:
                self.assertIsNone(pat.search(fh.read()), rel)


if __name__ == "__main__":
    unittest.main()
