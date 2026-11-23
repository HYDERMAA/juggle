"""Unit tests for skills/juggle/scripts/ledger.py."""
import io
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout, redirect_stderr

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "skills", "juggle", "scripts"))
import ledger  # noqa: E402


def run(path, *args):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = ledger.main(["--file", path, *args])
    return code, out.getvalue(), err.getvalue()


class LedgerLogic(unittest.TestCase):
    def test_numbering_and_default_status(self):
        items = []
        r1, _ = ledger.add(items, "Write the FAQ", "original")
        r2, _ = ledger.add(items, "Product description", "task")
        r3, _ = ledger.add(items, "British spelling", "rule")
        self.assertEqual([r1["id"], r2["id"], r3["id"]], ["R1", "R2", "R3"])
        self.assertEqual([r1["status"], r2["status"], r3["status"]], ["doing", "next", "active"])

    def test_first_task_starts_as_doing_when_nothing_is(self):
        items = []
        it, _ = ledger.add(items, "Only job", "task")
        self.assertEqual(it["status"], "doing")

    def test_repeat_message_is_one_request(self):
        items = []
        ledger.add(items, "also check none are taken on ebay", "task")
        it, new = ledger.add(items, "Also check none are taken on eBay!", "task")
        self.assertFalse(new)
        self.assertEqual(len(items), 1)

    def test_repeat_of_finished_request_is_new(self):
        items = []
        it, _ = ledger.add(items, "Run the tests", "task")
        ledger.set_status(items, it["id"], "done")
        _, new = ledger.add(items, "run the tests", "task")
        self.assertTrue(new)

    def test_bad_kind_status_and_empty(self):
        items = []
        with self.assertRaises(ValueError):
            ledger.add(items, "x", "banana")
        with self.assertRaises(ValueError):
            ledger.add(items, "   ", "task")
        ledger.add(items, "x", "task")
        with self.assertRaises(ValueError):
            ledger.set_status(items, "R1", "finished")
        with self.assertRaises(KeyError):
            ledger.set_status(items, "R9", "done")

    def test_ids_never_reused(self):
        items = []
        ledger.add(items, "a", "task"); ledger.add(items, "b", "task")
        items.pop(0)
        it, _ = ledger.add(items, "c", "task")
        self.assertEqual(it["id"], "R3")

    def test_open_items_and_summary(self):
        items = []
        ledger.add(items, "Email Printful", "original")
        ledger.add(items, "Changelog", "task")
        ledger.add(items, "No em dashes", "rule")
        ledger.add(items, "Refund policy", "task")
        ledger.set_status(items, "R1", "done", "500 tees, signed Hyder")
        ledger.set_status(items, "R4", "cancelled")
        self.assertEqual([i["id"] for i in ledger.open_items(items)], ["R2"])
        s = ledger.summary(items)
        self.assertIn("Done: R1 Email Printful (500 tees, signed Hyder)", s)
        self.assertIn("Cancelled: R4 Refund policy", s)
        self.assertIn("Rules: R3 No em dashes", s)


class LedgerFile(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmp.name, ".juggle", "ledger.md")

    def tearDown(self):
        self.tmp.cleanup()

    def test_round_trip_and_pipes_escaped(self):
        run(self.path, "add", "Fix A | B layout", "--kind", "original")
        run(self.path, "set", "R1", "done", "--note", "used grid | not flex")
        items = ledger.load(self.path)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["text"], "Fix A / B layout")
        self.assertEqual(items[0]["note"], "used grid / not flex")
        with open(self.path, encoding="utf-8") as fh:
            self.assertTrue(fh.read().startswith("# Juggle ledger"))

    def test_check_fails_while_open_and_passes_when_handled(self):
        run(self.path, "add", "Dark mode toggle", "--kind", "original")
        run(self.path, "add", "Save button on mobile")
        run(self.path, "add", "Ask which Brackwell", "--status", "needs-you")
        code, out, _ = run(self.path, "check")
        self.assertEqual(code, 1)
        self.assertIn("still open: R1", out)
        self.assertIn("still open: R2", out)
        self.assertIn("needs you: R3", out)
        run(self.path, "set", "R1", "done")
        run(self.path, "set", "R2", "cancelled")
        code, out, _ = run(self.path, "check")
        self.assertEqual(code, 0)
        self.assertIn("All requests handled", out)

    def test_set_unknown_id(self):
        code, _, err = run(self.path, "set", "R7", "done")
        self.assertEqual(code, 2)
        self.assertIn("no request R7", err)

    def test_clear_needs_yes_and_keeps_old(self):
        run(self.path, "add", "Something", "--kind", "original")
        code, _, _ = run(self.path, "clear")
        self.assertEqual(code, 2)
        self.assertEqual(len(ledger.load(self.path)), 1)
        code, _, _ = run(self.path, "clear", "--yes")
        self.assertEqual(code, 0)
        self.assertEqual(ledger.load(self.path), [])
        self.assertTrue(os.path.exists(os.path.join(os.path.dirname(self.path), "ledger-1.md")))

    def test_env_path(self):
        os.environ["JUGGLE_LEDGER"] = self.path
        try:
            self.assertEqual(ledger.default_path(), self.path)
        finally:
            del os.environ["JUGGLE_LEDGER"]

    def test_show_and_open_on_empty(self):
        code, out, _ = run(self.path, "show")
        self.assertEqual(code, 0)
        self.assertIn("No ledger yet", out)
        code, out, _ = run(self.path, "check")
        self.assertEqual(code, 0)
        self.assertIn("empty", out)


if __name__ == "__main__":
    unittest.main()
