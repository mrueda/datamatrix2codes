from __future__ import annotations

import csv
import io
import runpy
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest.mock import patch

from datamatrix2codes.cli import main, read_codes, write_results
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

    def test_empty_prefixed_visible_separator_and_ambiguous_inputs(self) -> None:
        empty = parse_encoded_string("  \n\t ")
        self.assertEqual(empty.STATUS, "UNPARSED")
        self.assertEqual(empty.EXPLAIN, "No scan was provided.")

        prefixed = parse_encoded_string("]d2010847000654766321ANT7T3KA31<GS>1726033110231853")
        self.assertEqual(prefixed.PC, "8470006547663")
        self.assertEqual(prefixed.SN, "ANT7T3KA31")
        self.assertEqual(prefixed.LOTE, "231853")
        self.assertEqual(prefixed.CAD, "2603")
        self.assertEqual(prefixed.STATUS, "OK")
        self.assertTrue(prefixed.HAS_GS)

        braced = parse_encoded_string("010847000654766321ANT7T3KA31{GS}1726033110231853")
        self.assertEqual(braced.STATUS, "OK")
        self.assertTrue(braced.HAS_GS)

        ambiguous = parse_encoded_string("010847000700681721AAAA171728110010LOT")
        self.assertEqual(ambiguous.PC, "8470007006817")
        self.assertEqual(ambiguous.SN, "")
        self.assertEqual(ambiguous.LOTE, "")
        self.assertEqual(ambiguous.CAD, "")
        self.assertEqual(ambiguous.STATUS, "AMBIGUOUS")
        self.assertEqual(ambiguous.CONFIDENCE, 55)
        self.assertEqual(ambiguous.EXPLAIN, "The scan can be interpreted in more than one way. Check the medicine box.")

    def test_invalid_dates_and_problematic_values_are_rejected(self) -> None:
        impossible_month = parse_encoded_string("010847000654766317991300")
        self.assertEqual(impossible_month.STATUS, "PARTIAL")
        self.assertEqual(impossible_month.PC, "8470006547663")
        self.assertEqual(impossible_month.CAD, "")

        impossible_day = parse_encoded_string("010847000654766317250230")
        self.assertEqual(impossible_day.STATUS, "PARTIAL")
        self.assertEqual(impossible_day.CAD, "")

        day_zero = parse_encoded_string("010847000654766317261100")
        self.assertEqual(day_zero.STATUS, "PARTIAL")
        self.assertEqual(day_zero.CAD, "2611")

        bad_gtin = parse_encoded_string("011234")
        self.assertEqual(bad_gtin.STATUS, "UNPARSED")

        duplicate_pc = parse_encoded_string("01084700065476630108470006547663")
        self.assertEqual(duplicate_pc.STATUS, "UNPARSED")
        self.assertEqual(duplicate_pc.PC, "")

        bad_serial_value = parse_encoded_string("010847000654766321ABC-DEF-XYZ")
        self.assertEqual(bad_serial_value.STATUS, "PARTIAL")
        self.assertEqual(bad_serial_value.SN, "")

    def test_cli_writes_review_columns(self) -> None:
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

    def test_cli_reads_header_custom_and_plain_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "in.csv"
            input_path.write_text("CODE\n010847000654766321ANT7T3KA311726033110231853\n", encoding="utf-8")
            codes = read_codes(input_path, None)

        self.assertEqual(codes, ["010847000654766321ANT7T3KA311726033110231853"])

        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "custom.csv"
            input_path.write_text("RAW,NOTE\n010847000654766321ANT7T3KA311726033110231853,ok\n,blank\n", encoding="utf-8")
            codes = read_codes(input_path, "RAW")

        self.assertEqual(codes, ["010847000654766321ANT7T3KA311726033110231853"])

        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "plain.csv"
            input_path.write_text("010847000654766321ANT7T3KA311726033110231853\n\n", encoding="utf-8")
            codes = read_codes(input_path, None)

        self.assertEqual(codes, ["010847000654766321ANT7T3KA311726033110231853"])

    def test_cli_rejects_missing_column(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "in.csv"
            input_path.write_text("OTHER\n010847000654766321ANT7T3KA311726033110231853\n", encoding="utf-8")
            with self.assertRaisesRegex(SystemExit, "Input CSV does not contain column 'CODE'"):
                read_codes(input_path, "CODE")

    def test_cli_main_success_and_io_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "in.csv"
            output_path = Path(tmpdir) / "out.csv"
            input_path.write_text("CODE\n010847000654766321ANT7T3KA311726033110231853\n", encoding="utf-8")

            self.assertEqual(main([str(input_path), str(output_path)]), 0)
            with output_path.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))

        self.assertEqual(rows[0]["PC"], "8470006547663")

        stderr = io.StringIO()
        with redirect_stderr(stderr):
            exit_code = main(["missing.csv", "out.csv"])
        self.assertEqual(exit_code, 1)
        self.assertIn("datamatrix2codes:", stderr.getvalue())

    def test_module_entrypoint(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "in.csv"
            output_path = Path(tmpdir) / "out.csv"
            input_path.write_text("CODE\n010847000654766321ANT7T3KA311726033110231853\n", encoding="utf-8")
            argv = ["python -m datamatrix2codes", str(input_path), str(output_path)]

            with patch.object(sys, "argv", argv), self.assertRaises(SystemExit) as raised:
                runpy.run_module("datamatrix2codes", run_name="__main__")

            self.assertEqual(raised.exception.code, 0)
            self.assertTrue(output_path.exists())


if __name__ == "__main__":
    unittest.main()
