#!/usr/bin/env python3
"""Synthetic tests: no real supplier documents or paths are used."""
import contextlib
import importlib.util
import io
from pathlib import Path
from unittest import TestCase, main, mock

spec = importlib.util.spec_from_file_location("history_audit", Path(__file__).with_name("audit-confidential-git-history.py"))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class HistoryAuditTests(TestCase):
    def run_case(self, responses):
        output = io.StringIO()
        with mock.patch.object(module, "git", side_effect=responses), contextlib.redirect_stdout(output):
            result = module.main()
        return result, output.getvalue()

    def test_shallow_history_fails_closed(self):
        code, log = self.run_case([b"true\n"])
        self.assertEqual(code, 1)
        self.assertIn("shallow", log)

    def test_empty_history_fails_closed(self):
        code, log = self.run_case([b"false\n", b""])
        self.assertEqual(code, 1)
        self.assertIn("no reachable commits", log)

    def test_historical_document_blocks_without_path_disclosure(self):
        path = "synthetic/confidential-vendor-contract.pdf"
        code, log = self.run_case([b"false\n", b"abc123\n", (path + "\0").encode()])
        self.assertEqual(code, 1)
        self.assertIn("1 restricted paths", log)
        self.assertNotIn(path, log)
        self.assertNotIn("vendor", log)

    def test_safe_history_passes(self):
        code, log = self.run_case([b"false\n", b"abc123\n", b"README.md\0"])
        self.assertEqual(code, 0)
        self.assertIn("PASS", log)

if __name__ == "__main__":
    main()
