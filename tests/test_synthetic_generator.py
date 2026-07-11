from __future__ import annotations

import csv
import io
import subprocess
import sys
import unittest
from pathlib import Path

from datamatrix2codes import parse_encoded_string


ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "tools" / "generate_synthetic_codes.py"


class SyntheticGeneratorTest(unittest.TestCase):
    def run_generator(self, *args: str) -> list[dict[str, str]]:
        completed = subprocess.run(
            [sys.executable, str(GENERATOR), *args],
            check=True,
            capture_output=True,
            text=True,
        )
        return list(csv.DictReader(io.StringIO(completed.stdout)))

    def assert_generated_rows_parse(self, rows: list[dict[str, str]]) -> None:
        self.assertGreater(len(rows), 0)
        statuses = {row["EXPECTED_STATUS"] for row in rows}
        self.assertIn("OK", statuses)
        self.assertIn("AMBIGUOUS", statuses)
        self.assertIn("PARTIAL", statuses)
        self.assertIn("UNPARSED", statuses)

        for row in rows:
            with self.subTest(case=row["CASE"]):
                parsed = parse_encoded_string(row["CODE"])
                self.assertEqual(parsed.STATUS, row["EXPECTED_STATUS"])
                self.assertEqual(parsed.PC, row["PC"])
                self.assertEqual(parsed.SN, row["SN"])
                self.assertEqual(parsed.LOTE, row["LOTE"])
                self.assertEqual(parsed.CAD, row["CAD"])

    def test_visible_separator_examples_parse_as_declared(self) -> None:
        rows = self.run_generator("--count", "12", "--separator", "visible")
        self.assert_generated_rows_parse(rows)

    def test_ascii29_separator_examples_parse_as_declared(self) -> None:
        rows = self.run_generator("--count", "8", "--separator", "ascii29")
        self.assert_generated_rows_parse(rows)

    def test_status_specific_ambiguous_examples_parse_as_declared(self) -> None:
        rows = self.run_generator("--count", "8", "--status", "ambiguous")
        self.assertEqual({row["EXPECTED_STATUS"] for row in rows}, {"AMBIGUOUS"})
        for row in rows:
            with self.subTest(case=row["CASE"]):
                parsed = parse_encoded_string(row["CODE"])
                self.assertEqual(parsed.STATUS, "AMBIGUOUS")
                self.assertEqual(parsed.PC, row["PC"])
                self.assertEqual(parsed.SN, "")
                self.assertEqual(parsed.LOTE, "")
                self.assertEqual(parsed.CAD, "")


if __name__ == "__main__":
    unittest.main()
