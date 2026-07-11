"""GS1-aware parser with recovery for scanner strings missing separators."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import re

GROUP_SEPARATOR = "\x1d"

TARGET_FIELDS = ("PC", "SN", "LOTE", "CAD")


@dataclass(frozen=True)
class ParseResult:
    PC: str = ""
    SN: str = ""
    LOTE: str = ""
    CAD: str = ""
    STATUS: str = "UNPARSED"
    CONFIDENCE: int = 0
    HAS_GS: bool = False
    EXPLAIN: str = "No scan was provided."


@dataclass(frozen=True)
class Candidate:
    fields: tuple[tuple[str, str], ...] = ()
    ignored_71: int = 0
    leftover: str = ""

    def as_dict(self) -> dict[str, str]:
        return dict(self.fields)

    def with_field(self, name: str, value: str) -> "Candidate":
        data = self.as_dict()
        if name in data:
            return Candidate(self.fields, self.ignored_71, "DUPLICATE")
        data[name] = value
        return Candidate(tuple(sorted(data.items())), self.ignored_71, self.leftover)

    def with_ignored_71(self) -> "Candidate":
        return Candidate(self.fields, self.ignored_71 + 1, self.leftover)

    def with_leftover(self, leftover: str) -> "Candidate":
        return Candidate(self.fields, self.ignored_71, leftover)


def parse_encoded_string(encoded: str) -> ParseResult:
    has_gs = has_group_separator(encoded)
    normalized = normalize_input(encoded)
    if not normalized:
        return ParseResult(HAS_GS=has_gs)

    candidates = parse_candidates(normalized)
    if not candidates:
        return ParseResult(
            STATUS="UNPARSED",
            HAS_GS=has_gs,
            EXPLAIN="The scan could not be decoded. Check the scanner input or enter the values manually.",
        )

    ranked = sorted(candidates, key=score_candidate, reverse=True)
    best = ranked[0]
    best_score = score_candidate(best)
    comparable = [candidate for candidate in ranked if score_candidate(candidate) == best_score]
    fields = best.as_dict()

    ambiguous = False
    if not any(fields.get(name) for name in TARGET_FIELDS):
        status = "UNPARSED"
    else:
        status = "OK" if all(fields.get(name) for name in TARGET_FIELDS) and not best.leftover else "PARTIAL"
    if any(candidate.as_dict() != fields for candidate in comparable):
        status = "AMBIGUOUS"
        ambiguous = True
        fields = blank_disputed_fields(comparable)

    confidence = confidence_for(status, fields, best.leftover)
    explain = explain_result(status, fields, best.leftover, has_gs, ambiguous)

    return ParseResult(
        PC=fields.get("PC", ""),
        SN=fields.get("SN", ""),
        LOTE=fields.get("LOTE", ""),
        CAD=fields.get("CAD", ""),
        STATUS=status,
        CONFIDENCE=confidence,
        HAS_GS=has_gs,
        EXPLAIN=explain,
    )


def has_group_separator(encoded: str) -> bool:
    value = str(encoded or "")
    return GROUP_SEPARATOR in value or "<GS>" in value or "{GS}" in value


def normalize_input(encoded: str) -> str:
    value = str(encoded or "").strip()
    if value.startswith("]d2"):
        value = value[3:]
    value = value.replace("<GS>", GROUP_SEPARATOR)
    value = value.replace("{GS}", GROUP_SEPARATOR)
    value = re.sub(r"[\s\r\n\t]+", "", value)
    return value


def parse_candidates(value: str) -> list[Candidate]:
    @lru_cache(maxsize=None)
    def walk(pos: int) -> tuple[Candidate, ...]:
        if pos >= len(value):
            return (Candidate(),)

        if value[pos] == GROUP_SEPARATOR:
            return walk(pos + 1)

        results: list[Candidate] = []

        if value.startswith("01", pos):
            gtin = value[pos + 2 : pos + 16]
            if len(gtin) == 14 and gtin.isdigit():
                for rest in walk(pos + 16):
                    add_candidate(results, rest.with_field("PC", normalize_gtin(gtin)))

        if value.startswith("17", pos):
            expiry = value[pos + 2 : pos + 8]
            if len(expiry) == 6 and expiry.isdigit() and valid_expiry(expiry):
                for rest in walk(pos + 8):
                    add_candidate(results, rest.with_field("CAD", expiry[:4]))

        if value.startswith("71", pos):
            nhrn = value[pos + 2 : pos + 10]
            if len(nhrn) == 8 and nhrn.isdigit():
                for rest in walk(pos + 10):
                    add_candidate(results, rest.with_ignored_71())

        if value.startswith("10", pos):
            results.extend(parse_variable(value, walk, pos + 2, "LOTE", 3, 20))

        if value.startswith("21", pos):
            results.extend(parse_variable(value, walk, pos + 2, "SN", 8, 20))

        if not results:
            return (Candidate(leftover=value[pos:]),)

        return tuple(results)

    return list(walk(0))


def parse_variable(value: str, walk, start: int, field: str, min_len: int, max_len: int) -> list[Candidate]:
    results: list[Candidate] = []
    limit = min(max_len, len(value) - start)

    if GROUP_SEPARATOR in value[start : start + limit + 1]:
        sep = value.find(GROUP_SEPARATOR, start)
        if min_len <= sep - start <= max_len:
            item = value[start:sep]
            if valid_variable_value(item):
                for rest in walk(sep + 1):
                    add_candidate(results, rest.with_field(field, item))
        return results

    for length in range(min_len, limit + 1):
        item = value[start : start + length]
        if not valid_variable_value(item):
            continue
        for rest in walk(start + length):
            add_candidate(results, rest.with_field(field, item))

    return results


def add_candidate(results: list[Candidate], candidate: Candidate) -> None:
    if candidate.leftover == "DUPLICATE":
        return
    results.append(candidate)


def normalize_gtin(gtin: str) -> str:
    return gtin[1:] if gtin.startswith("0") else gtin


def valid_variable_value(value: str) -> bool:
    return bool(value) and all(char.isalnum() for char in value)


def valid_expiry(expiry: str) -> bool:
    year = int(expiry[:2])
    month = int(expiry[2:4])
    day = int(expiry[4:6])
    if not 1 <= month <= 12:
        return False
    if day == 0:
        return True
    month_days = [31, 29 if year % 4 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return day <= month_days[month - 1]


def gtin_check_digit_ok(pc: str) -> bool:
    gtin = pc if len(pc) == 14 else f"0{pc}" if len(pc) == 13 else pc
    if len(gtin) != 14 or not gtin.isdigit():
        return False
    digits = [int(char) for char in gtin]
    total = sum(digit * (3 if idx % 2 == 0 else 1) for idx, digit in enumerate(digits[-2::-1]))
    return (10 - total % 10) % 10 == digits[-1]


def score_candidate(candidate: Candidate) -> tuple[int, int, int, int, int]:
    fields = candidate.as_dict()
    complete = int(all(fields.get(name) for name in TARGET_FIELDS))
    count = sum(1 for name in TARGET_FIELDS if fields.get(name))
    quality = 0

    if fields.get("PC") and gtin_check_digit_ok(fields["PC"]):
        quality += 20
    if fields.get("CAD"):
        quality += 10
    if fields.get("LOTE"):
        quality -= variable_penalty("LOTE", fields["LOTE"])
    if fields.get("SN"):
        quality -= variable_penalty("SN", fields["SN"])

    no_leftover = int(candidate.leftover == "")
    ignored = candidate.ignored_71
    compactness = -sum(len(value) for name, value in fields.items() if name in ("SN", "LOTE"))
    return (complete, count, no_leftover, ignored, quality + compactness)


def variable_penalty(name: str, value: str) -> int:
    penalty = 0
    if name == "LOTE" and value.startswith(("10", "17", "21", "71")):
        penalty += 30
    if name == "SN" and value.startswith(("10", "17")):
        penalty += 10
    return penalty


def blank_disputed_fields(candidates: list[Candidate]) -> dict[str, str]:
    resolved: dict[str, str] = {}
    for name in TARGET_FIELDS:
        values = {candidate.as_dict().get(name, "") for candidate in candidates}
        resolved[name] = values.pop() if len(values) == 1 else ""
    return resolved


def confidence_for(status: str, fields: dict[str, str], leftover: str) -> int:
    if status == "OK":
        return 100
    if status == "AMBIGUOUS":
        agreed = sum(1 for name in TARGET_FIELDS if fields.get(name))
        return 45 + agreed * 10
    if status == "PARTIAL":
        parsed = sum(1 for name in TARGET_FIELDS if fields.get(name))
        penalty = 10 if leftover else 0
        return max(20, parsed * 20 - penalty)
    return 0


def explain_result(status: str, fields: dict[str, str], leftover: str, has_gs: bool, ambiguous: bool) -> str:
    if status == "OK":
        return "Code read correctly with scanner separators." if has_gs else "Code read correctly."
    if ambiguous:
        return "The scan can be interpreted in more than one way. Check the medicine box."
    if status == "PARTIAL":
        return "Some fields could not be found. Review this row."
    return "The scan could not be decoded. Check the scanner input or enter the values manually."
