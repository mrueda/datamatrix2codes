# Parser Notes

The parser recognizes these target GS1 Application Identifiers:

| AI | Field | Rule |
| --- | --- | --- |
| `01` | `PC` | Fixed 14-digit GTIN, normalized by stripping one leading zero when present. |
| `17` | `CAD` | Fixed expiry date `YYMMDD`, output as `YYMM`. |
| `10` | `LOTE` | Variable-length alphanumeric lot. |
| `21` | `SN` | Variable-length alphanumeric serial number. |

It also recognizes `71` followed by eight digits as an ignored healthcare/NHRN-style segment when recovering fields from flattened strings.

## Strict Parsing

When ASCII 29 group separators are present, variable-length fields stop at the separator. This is the most reliable path.

## Recovery Parsing

When separators are missing, the parser tries candidate field boundaries and scores them. It prefers complete parses, valid GTIN check digits, valid expiry dates, no leftover text, and recognized healthcare segments.

Some flattened strings are genuinely ambiguous. The parser should surface uncertainty instead of silently inventing a value.

## Ambiguity Example

A flattened scan can contain an Application Identifier-like fragment inside a real value:

```text
...21SYNTH17VALUE1728110010AD801
```

The parser has to decide whether the first `17` is part of the serial number or the start of the expiry-date field. If the encoded group separator had reached Excel, the boundary would be explicit:

```text
...21SYNTH17VALUE<GS>1728110010AD801
```

Without that separator, the parser tries candidate boundaries and validates them. A valid expiry must be six digits after `17`; a GTIN must have the expected length and check digit; variable fields must stay within supported lengths.

If one interpretation satisfies the rules clearly, the parser returns `OK`. If top candidates remain equally plausible and disagree on a field, the parser returns `AMBIGUOUS`, keeps agreed fields, and leaves disputed fields blank.
