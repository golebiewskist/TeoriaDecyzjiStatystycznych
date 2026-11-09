"""Check a saved report using three synthetic messages: two ham and one spam."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


PROJECT = Path(__file__).resolve().parents[1]
FIXTURE = PROJECT / "tests" / "fixtures" / "messages.csv"


class ReportTest(unittest.TestCase):
    def test_cli_writes_expected_counts(self):
        """The CLI saves a report for the intended input with counts 3 / 2 / 1."""
        with tempfile.TemporaryDirectory(prefix="spam-lab-test-") as directory:
            output = Path(directory) / "summary.json"
            result = subprocess.run(
                [sys.executable, str(PROJECT / "describe_data.py"),
                 "--data", str(FIXTURE), "--out", str(output)],
                cwd=PROJECT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue(output.is_file(), "The program did not save a report.")
            report = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(report["input_file"], str(FIXTURE))
            self.assertEqual(report["total_messages"], 3)
            self.assertEqual(report["label_counts"], {"ham": 2, "spam": 1})


if __name__ == "__main__":
    unittest.main()
