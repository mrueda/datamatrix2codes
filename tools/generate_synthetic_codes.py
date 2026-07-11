#!/usr/bin/env python3
"""Generate safe synthetic GS1 DataMatrix-like payloads for tests and demos."""

from __future__ import annotations

import argparse
import csv
import random
import sys
from dataclasses import dataclass
from pathlib import Path

GROUP_SEPARATOR = "\x1d"


@dataclass(frozen=True)
class SyntheticCode:
    case: str
    code: str
    pc: str
    sn: str
    lote: str
    cad: str
    expected_status: str
    note: str


def gtin_check_digit(first_13_digits: str) -> str:
    if len(first_13_digits) != 13 or not first_13_digits.isdigit():
        raise ValueError("GTIN-14 seed must contain exactly 13 digits")
    digits = [int(char) for char in first_13_digits]
    total = sum(digit * (3 if idx % 2 == 0 else 1) for idx, digit in enumerate(reversed(digits)))
    return str((10 - total % 10) % 10)


def make_gtin(index: int) -> str:
    seed = f"0849999{index:06d}"
    return seed + gtin_check_digit(seed)


def normalize_pc(gtin: str) -> str:
    return gtin[1:] if gtin.startswith("0") else gtin


def separator_for(mode: str, rng: random.Random) -> str:
    if mode == "none":
        return ""
    if mode == "visible":
        return "<GS>"
    if mode == "ascii29":
        return GROUP_SEPARATOR
    return rng.choice(["", "<GS>", GROUP_SEPARATOR])


def fixed_examples(separator_mode: str, rng: random.Random) -> list[SyntheticCode]:
    gtin1 = make_gtin(1)
    gtin2 = make_gtin(2)
    gtin3 = make_gtin(3)

    clean_separator = "<GS>" if separator_mode != "ascii29" else GROUP_SEPARATOR
    flattened_code = f"01{gtin2}21SYNTH1231728123110LOT123"

    return [
        SyntheticCode(
            case="clean_with_separator",
            code=f"01{gtin1}21SNSAFE01{clean_separator}1728123110LOTSAFE",
            pc=normalize_pc(gtin1),
            sn="SNSAFE01",
            lote="LOTSAFE",
            cad="2812",
            expected_status="OK",
            note="A scanner/app preserved an explicit GS1 field separator.",
        ),
        SyntheticCode(
            case="clean_flattened",
            code=flattened_code,
            pc=normalize_pc(gtin2),
            sn="SYNTH123",
            lote="LOT123",
            cad="2812",
            expected_status="OK",
            note="A flattened payload that still has one clear interpretation.",
        ),
        SyntheticCode(
            case="ambiguous_flattened",
            code=f"01{gtin3}21AAAA171728110010LOT",
            pc=normalize_pc(gtin3),
            sn="",
            lote="",
            cad="",
            expected_status="AMBIGUOUS",
            note="The same digits can be read as field starts or value text.",
        ),
        SyntheticCode(
            case="partial_missing_fields",
            code=f"01{gtin1}21SNONLY01",
            pc=normalize_pc(gtin1),
            sn="SNONLY01",
            lote="",
            cad="",
            expected_status="PARTIAL",
            note="Only PC and serial can be recovered.",
        ),
        SyntheticCode(
            case="unparsed_text",
            code="not-a-gs1-datamatrix-payload",
            pc="",
            sn="",
            lote="",
            cad="",
            expected_status="UNPARSED",
            note="A non-GS1 scanner string.",
        ),
    ]


def generated_ok_examples(count: int, separator_mode: str, rng: random.Random) -> list[SyntheticCode]:
    rows: list[SyntheticCode] = []
    for offset in range(count):
        index = offset + 100
        gtin = make_gtin(index)
        sn = f"S{index:07d}"
        lote = f"L{index:05d}"
        expiry = f"{28 + offset % 5:02d}{1 + offset % 12:02d}00"
        sep = separator_for(separator_mode, rng)
        code = f"01{gtin}21{sn}{sep}17{expiry}10{lote}"
        rows.append(
            SyntheticCode(
                case=f"generated_ok_{offset + 1:03d}",
                code=code,
                pc=normalize_pc(gtin),
                sn=sn,
                lote=lote,
                cad=expiry[:4],
                expected_status="OK",
                note="Deterministic synthetic payload.",
            )
        )
    return rows


def generated_ambiguous_examples(count: int) -> list[SyntheticCode]:
    rows: list[SyntheticCode] = []
    for offset in range(count):
        index = offset + 200
        gtin = make_gtin(index)
        code = f"01{gtin}21AAAA1728110010LOT"
        rows.append(
            SyntheticCode(
                case=f"generated_ambiguous_{offset + 1:03d}",
                code=code,
                pc=normalize_pc(gtin),
                sn="",
                lote="",
                cad="",
                expected_status="AMBIGUOUS",
                note="Flattened payload where serial, expiry, and lot boundaries overlap.",
            )
        )
    return rows


def generated_partial_examples(count: int) -> list[SyntheticCode]:
    rows: list[SyntheticCode] = []
    for offset in range(count):
        index = offset + 300
        gtin = make_gtin(index)
        sn = f"SNONLY{offset + 1:02d}"
        rows.append(
            SyntheticCode(
                case=f"generated_partial_{offset + 1:03d}",
                code=f"01{gtin}21{sn}",
                pc=normalize_pc(gtin),
                sn=sn,
                lote="",
                cad="",
                expected_status="PARTIAL",
                note="Payload with PC and serial only.",
            )
        )
    return rows


def generated_unparsed_examples(count: int) -> list[SyntheticCode]:
    return [
        SyntheticCode(
            case=f"generated_unparsed_{offset + 1:03d}",
            code=f"not-a-gs1-datamatrix-payload-{offset + 1:03d}",
            pc="",
            sn="",
            lote="",
            cad="",
            expected_status="UNPARSED",
            note="Plain text that is not a supported GS1 DataMatrix payload.",
        )
        for offset in range(count)
    ]


def generate_codes(count: int, seed: int, separator_mode: str, status: str) -> list[SyntheticCode]:
    rng = random.Random(seed)
    if status == "ok":
        return generated_ok_examples(count, separator_mode, rng)
    if status == "ambiguous":
        return generated_ambiguous_examples(count)
    if status == "partial":
        return generated_partial_examples(count)
    if status == "unparsed":
        return generated_unparsed_examples(count)

    rows = fixed_examples(separator_mode, rng)
    if count <= len(rows):
        return rows[:count]
    rows.extend(generated_ok_examples(count - len(rows), separator_mode, rng))
    return rows


def write_csv(rows: list[SyntheticCode], output: Path | None) -> None:
    handle = output.open("w", newline="", encoding="utf-8") if output else sys.stdout
    try:
        writer = csv.writer(handle)
        writer.writerow(["CASE", "CODE", "PC", "SN", "LOTE", "CAD", "EXPECTED_STATUS", "NOTE"])
        for row in rows:
            writer.writerow(
                [row.case, row.code, row.pc, row.sn, row.lote, row.cad, row.expected_status, row.note]
            )
    finally:
        if output:
            handle.close()


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate synthetic GS1 DataMatrix-like scanner strings for datamatrix2codes."
    )
    parser.add_argument("--count", type=int, default=20, help="number of rows to generate")
    parser.add_argument("--seed", type=int, default=20260711, help="deterministic random seed")
    parser.add_argument(
        "--separator",
        choices=["mixed", "none", "visible", "ascii29"],
        default="visible",
        help="how to represent the GS1 group separator in generated OK rows",
    )
    parser.add_argument(
        "--status",
        choices=["all", "ok", "ambiguous", "partial", "unparsed"],
        default="all",
        help="generate all example types or only rows with one expected parser status",
    )
    parser.add_argument("--output", type=Path, help="write CSV to this path instead of stdout")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.count < 1:
        raise SystemExit("--count must be at least 1")
    rows = generate_codes(args.count, args.seed, args.separator, args.status)
    write_csv(rows, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
