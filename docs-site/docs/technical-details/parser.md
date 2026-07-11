# Parser Notes

The parser recognizes these target GS1 Application Identifiers:

| AI | Field | Rule |
| --- | --- | --- |
| `01` | `PC` | Fixed 14-digit GTIN, normalized by stripping one leading zero when present. |
| `17` | `CAD` | Fixed expiry date `YYMMDD`, output as `YYMM`. |
| `10` | `LOTE` | Variable-length lot. Printable characters are accepted because SEVeM scanner validation examples include spaces and punctuation. |
| `21` | `SN` | Variable-length serial number. Printable characters are accepted because SEVeM scanner validation examples include spaces and punctuation. |

It also recognizes `71` followed by eight digits as an ignored healthcare/NHRN-style segment when recovering fields from flattened strings.

## Strict Parsing

When ASCII 29 group separators are present, variable-length fields stop at the separator. This is the most reliable path.

## Recovery Parsing

When separators are missing, the parser tries candidate field boundaries and scores them. It prefers complete parses, valid GTIN check digits, valid expiry dates, no leftover text, and recognized healthcare segments.

Some flattened strings are genuinely ambiguous. The parser should surface uncertainty instead of silently inventing a value.

## Ambiguity Example

A flattened scan can contain the same digit sequence inside a real value and at a field boundary:

```text
...21SYNTH17VALUE1728110010AD801
```

The parser has to decide whether the first `17` is part of the serial number or the start of the expiry-date field. If the encoded group separator had reached Excel, the boundary would be explicit:

```text
...21SYNTH17VALUE<GS>1728110010AD801
```

`<GS>` is documentation notation for the GS1 group separator. The actual scanner string may contain ASCII 29, visible `GS` as shown in SEVeM scanner validation examples, another replacement such as `<GS>`, `{GS}`, `'`, or `|`, or no visible separator character at all.

Without that separator, the parser tries candidate boundaries and validates them. A valid expiry must be six digits after `17`; a GTIN must have the expected length and check digit; variable fields must stay within supported lengths.

If one interpretation satisfies the rules clearly, the parser returns `OK`. If candidates remain plausible and disagree on a field, the parser returns `AMBIGUOUS`, keeps agreed fields, and leaves disputed fields blank.
