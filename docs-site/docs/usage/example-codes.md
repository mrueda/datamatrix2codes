# Example Codes

These examples show what a pharmacist should expect after a scanner writes a raw string into Excel and the workbook runs `ParseEncodedString`.

The strings below are synthetic documentation examples. They are shaped like scanner output, but they are not real pack serials.

`<GS>` means a visible placeholder for the GS1 group separator. Real Excel input may contain ASCII 29, visible `GS` as shown in SEVeM scanner validation examples, another replacement such as `<GS>`, `{GS}`, `'`, or `|`, or no visible separator character.

| Raw scanner string | PC | SN | LOTE | CAD | STATUS | CONFIDENCE | HAS_GS |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `010847000654766321ANT7T3KA31<GS>1726033110231853` | `8470006547663` | `ANT7T3KA31` | `231853` | `2603` | `OK` | `100` | `TRUE` |
| `010843523234741821AWF6VCKB8F2S10AD80117281100` | `8435232347418` | `AWF6VCKB8F2S` | `AD801` | `2811` | `OK` | `100` | `FALSE` |
| `010847000700681721SYNTH17VALUE1728110010AD801` | `8470007006817` | `SYNTH17VALUE` | `AD801` | `2811` | `OK` | `100` | `FALSE` |
| `010847000654766321ANT7T3KA31` | `8470006547663` | `ANT7T3KA31` | `(blank)` | `(blank)` | `PARTIAL` | `40` | `FALSE` |
| `010847000700681721AAAA171728110010LOT` | `8470007006817` | `(blank)` | `(blank)` | `(blank)` | `AMBIGUOUS` | `55` | `FALSE` |
| `third-party-scanner-text-not-supported` | `(blank)` | `(blank)` | `(blank)` | `(blank)` | `UNPARSED` | `0` | `FALSE` |

## How To Read The Table

`OK` means the parser found all four target fields: `PC`, `SN`, `LOTE`, and `CAD`.

`PARTIAL` means the string contains some usable fields, but not enough for a complete row.

`AMBIGUOUS` means the flattened scanner string has more than one plausible interpretation. In that case, disputed fields are left blank so the row is reviewed instead of silently choosing a risky answer.

`UNPARSED` means the scan could not be decoded into the supported Data Matrix fields. It does not prove that the medicine code itself is invalid.

## Same Examples As Formulas

If the raw string is in `A2`, the table columns come from formulas like:

```excel
=ParseEncodedString(A2,"PC")
=ParseEncodedString(A2,"SN")
=ParseEncodedString(A2,"LOTE")
=ParseEncodedString(A2,"CAD")
=ParseEncodedString(A2,"STATUS")
=ParseEncodedString(A2,"CONFIDENCE")
=ParseEncodedString(A2,"HAS_GS")
```

If Excel rejects those formulas, use semicolons instead of commas:

```excel
=ParseEncodedString(A2;"PC")
```

## Generate Safe Test Codes

Do not publish real medicine-pack serials in issues, screenshots, or test fixtures. For demos and regression tests, generate synthetic scanner strings from the repository root:

```bash
python3 tools/generate_synthetic_codes.py --count 20 > synthetic-codes.csv
```

The generated CSV includes the raw `CODE`, the expected parsed fields, and the expected parser status. It deliberately includes clean, flattened, partial, ambiguous, and unparsed examples.

To generate only ambiguous examples:

```bash
python3 tools/generate_synthetic_codes.py --status ambiguous --count 20 > ambiguous-codes.csv
```

To generate rows containing a real ASCII 29 GS1 group separator instead of visible `<GS>` text:

```bash
python3 tools/generate_synthetic_codes.py --count 20 --separator ascii29 > synthetic-codes.csv
```
