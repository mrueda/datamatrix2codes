"""Parse GS1 DataMatrix strings used on medicinal product packages."""

from .parser import ParseResult, parse_encoded_string

__all__ = ["ParseResult", "parse_encoded_string"]
