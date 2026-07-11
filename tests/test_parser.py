from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

from datamatrix2codes.cli import read_codes, write_results
from datamatrix2codes import parse_encoded_string


ROOT = Path(__file__).resolve().parents[1]


MONTHS = {
    "Jan": "01",
    "Feb": "02",
    "Mar": "03",
    "Apr": "04",
    "May": "05",
    "Jun": "06",
    "Jul": "07",
    "Aug": "08",
    "Sep": "09",
    "Oct": "10",
    "Nov": "11",
    "Dec": "12",
}


def load_expected() -> list[dict[str, str]]:
    expected: list[dict[str, str]] = []
    with (ROOT / "data" / "results.tsv").open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle, delimiter="\t")
        for row in reader:
            month, year = row[3].split("-")
            expected.append({"PC": row[0], "SN": row[1], "LOTE": row[2], "CAD": year + MONTHS[month]})
    return expected


class ParserFixtureTest(unittest.TestCase):
    def test_current_fixture(self) -> None:
        codes = (ROOT / "data" / "codes.csv").read_text(encoding="utf-8").splitlines()
        expected = load_expected()

        self.assertEqual(len(codes), len(expected))
        for row_number, (code, wanted) in enumerate(zip(codes, expected), start=1):
            with self.subTest(row=row_number, code=code):
                parsed = parse_encoded_string(code)
                self.assertEqual(parsed.PC, wanted["PC"])
                self.assertEqual(parsed.SN, wanted["SN"])
                self.assertEqual(parsed.LOTE, wanted["LOTE"])
                self.assertEqual(parsed.CAD, wanted["CAD"])
                self.assertEqual(parsed.STATUS, "OK")
                self.assertEqual(parsed.CONFIDENCE, 100)
                self.assertFalse(parsed.HAS_GS)
                self.assertEqual(parsed.EXPLAIN, "Code read correctly.")

    def test_group_separator_strict_parse(self) -> None:
        parsed = parse_encoded_string("010847000654766321ANT7T3KA31\x1d1726033110231853")
        self.assertEqual(parsed.PC, "8470006547663")
        self.assertEqual(parsed.SN, "ANT7T3KA31")
        self.assertEqual(parsed.CAD, "2603")
        self.assertEqual(parsed.LOTE, "231853")
        self.assertEqual(parsed.STATUS, "OK")
        self.assertEqual(parsed.CONFIDENCE, 100)
        self.assertTrue(parsed.HAS_GS)
        self.assertEqual(parsed.EXPLAIN, "Code read correctly with scanner separators.")

    def test_known_old_failure_cases_are_fixed(self) -> None:
        cases = [
            (
                "010847000700681721PE42EEADPA9HW41728033110V067127006817",
                {"PC": "8470007006817", "SN": "PE42EEADPA9HW4", "LOTE": "V06", "CAD": "2803"},
            ),
            (
                "01189010791063361726103110HFZ022058218058271392047127035497",
                {"PC": "18901079106336", "SN": "805827139204", "LOTE": "HFZ022058", "CAD": "2610"},
            ),
            (
                "0108470007210764211002664707361010A59112B17260430",
                {"PC": "8470007210764", "SN": "10026647073610", "LOTE": "A59112B", "CAD": "2604"},
            ),
        ]

        for code, wanted in cases:
            with self.subTest(code=code):
                parsed = parse_encoded_string(code)
                self.assertEqual(parsed.PC, wanted["PC"])
                self.assertEqual(parsed.SN, wanted["SN"])
                self.assertEqual(parsed.LOTE, wanted["LOTE"])
                self.assertEqual(parsed.CAD, wanted["CAD"])
                self.assertEqual(parsed.STATUS, "OK")
                self.assertEqual(parsed.CONFIDENCE, 100)

    def test_partial_and_unparsed_statuses(self) -> None:
        partial = parse_encoded_string("010847000654766321ANT7T3KA31")
        self.assertEqual(partial.PC, "8470006547663")
        self.assertEqual(partial.SN, "ANT7T3KA31")
        self.assertEqual(partial.LOTE, "")
        self.assertEqual(partial.CAD, "")
        self.assertEqual(partial.STATUS, "PARTIAL")
        self.assertLess(partial.CONFIDENCE, 100)
        self.assertEqual(partial.EXPLAIN, "Some fields could not be found. Review this row.")

        unparsed = parse_encoded_string("hello")
        self.assertEqual(unparsed.PC, "")
        self.assertEqual(unparsed.SN, "")
        self.assertEqual(unparsed.LOTE, "")
        self.assertEqual(unparsed.CAD, "")
        self.assertEqual(unparsed.STATUS, "UNPARSED")
        self.assertEqual(unparsed.CONFIDENCE, 0)
        self.assertEqual(unparsed.EXPLAIN, "The scan could not be decoded. Check the scanner input or enter the values manually.")

    def test_cli_writes_feedback_columns(self) -> None:
        codes = ["010847000654766321ANT7T3KA311726033110231853"]
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "out.csv"
            write_results(output, codes)
            with output.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["STATUS"], "OK")
        self.assertEqual(rows[0]["CONFIDENCE"], "100")
        self.assertEqual(rows[0]["HAS_GS"], "FALSE")
        self.assertEqual(rows[0]["EXPLAIN"], "Code read correctly.")

    def test_cli_reads_header_code_column(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "in.csv"
            input_path.write_text("CODE\n010847000654766321ANT7T3KA311726033110231853\n", encoding="utf-8")
            codes = read_codes(input_path, None)

        self.assertEqual(codes, ["010847000654766321ANT7T3KA311726033110231853"])


if __name__ == "__main__":
    unittest.main()
