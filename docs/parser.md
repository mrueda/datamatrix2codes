# Parser Notes

GS1 DataMatrix payloads use Application Identifiers. This project currently cares about four target fields.

| AI | Field | Rule |
| --- | --- | --- |
| `01` | `PC` | Fixed 14 numeric GTIN. A single leading zero is stripped for the output field. |
| `17` | `CAD` | Fixed 6 numeric expiry date `YYMMDD`; output is `YYMM`. |
| `10` | `LOTE` | Variable-length alphanumeric value. |
| `21` | `SN` | Variable-length alphanumeric value. |

The parser also recognizes `71` followed by eight digits as an ignored healthcare/NHRN-style segment. This appears in the fixture data and helps recover the target fields.

## Strict Mode

Strict parsing consumes the string from left to right. Fixed-length fields are read by length. Variable-length fields stop at the ASCII group separator, character 29, when present.

The parser accepts scanner text forms `<GS>` and `{GS}` and converts them to the group separator internally.

## Recovery Mode

The original pharmacy scanner output omitted group separators, and the fixture data intentionally keeps that flattened form. In that case, a value may contain text that looks like another AI, such as `17` inside a product code or `10` inside a serial number.

Recovery mode tries multiple candidate boundaries and scores them. It prefers:

- all four fields present;
- valid GTIN check digit;
- valid expiry date;
- no leftover text;
- recognized `71` segments;
- shorter plausible variable-length fields when all else is equal.

If top-scoring candidates disagree, disputed fields are blank and `STATUS` is `AMBIGUOUS`.

## Limits

Some strings are genuinely ambiguous without the original group separators or additional product knowledge. The parser is designed to avoid silent wrong guesses in those cases.
