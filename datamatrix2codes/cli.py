"""Command line interface for datamatrix2codes."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

from .parser import parse_encoded_string


def read_codes(path: Path, column: str | None) -> list[str]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        sample = handle.read(2048)
        handle.seek(0)
        try:
            has_header = csv.Sniffer().has_header(sample) if sample.strip() else False
        except csv.Error:
            has_header = False
        first_line = sample.splitlines()[0].strip().lstrip("\ufeff") if sample.splitlines() else ""
        if first_line.upper() == (column or "CODE").upper():
            has_header = True

        if column or has_header:
            reader = csv.DictReader(handle)
            wanted = column or "CODE"
            if not reader.fieldnames or wanted not in reader.fieldnames:
                names = ", ".join(reader.fieldnames or [])
                raise SystemExit(f"Input CSV does not contain column {wanted!r}. Found: {names}")
            return [row[wanted].strip() for row in reader if row.get(wanted, "").strip()]

        reader = csv.reader(handle)
        return [row[0].strip() for row in reader if row and row[0].strip()]


def write_results(path: Path, codes: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["CODE", "PC", "SN", "LOTE", "CAD", "STATUS", "CONFIDENCE", "HAS_GS", "EXPLAIN"],
        )
        writer.writeheader()
        for code in codes:
            parsed = parse_encoded_string(code)
            writer.writerow(
                {
                    "CODE": code,
                    "PC": parsed.PC,
                    "SN": parsed.SN,
                    "LOTE": parsed.LOTE,
                    "CAD": parsed.CAD,
                    "STATUS": parsed.STATUS,
                    "CONFIDENCE": parsed.CONFIDENCE,
                    "HAS_GS": "TRUE" if parsed.HAS_GS else "FALSE",
                    "EXPLAIN": parsed.EXPLAIN,
                }
            )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="datamatrix2codes",
        description="Extract PC, SN, LOTE, and CAD from raw GS1 DataMatrix strings.",
    )
    parser.add_argument("input_csv", type=Path, help="Input CSV, either one code per row or a CODE column.")
    parser.add_argument("output_csv", type=Path, help="Output CSV path.")
    parser.add_argument("--column", help="Input column name when the CSV has headers. Defaults to CODE.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        codes = read_codes(args.input_csv, args.column)
        write_results(args.output_csv, codes)
    except OSError as exc:
        print(f"datamatrix2codes: {exc}", file=sys.stderr)
        return 1

    return 0
