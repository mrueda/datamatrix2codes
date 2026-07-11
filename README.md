# datamatrix2codes

`datamatrix2codes` extracts pharmacy fields from GS1 DataMatrix scans on medicinal product packages.

This project exists because the hard part is often not the DataMatrix symbol itself. The hard part is what happens after the scanner decodes it and sends a one-line string into Excel.

| Field | Meaning | GS1 AI |
| --- | --- | --- |
| `PC` | Código Nacional / product code, normalized from GTIN | `01` |
| `SN` | Serial number | `21` |
| `LOTE` | Batch / lot number | `10` |
| `CAD` | Expiry date as `YYMM` | `17` |

## Spanish Pharmacy Terms

In Spain, when it comes to medicinal products and their packaging, especially the data encoded in GS1 DataMatrix 2D barcodes, the following terms are commonly used:

- `PC` (`Código Nacional`): the National Code. It identifies a specific drug product in Spain and helps with quick identification and verification.
- `CAD` (`Fecha de Caducidad`): the expiry date. It indicates until when the drug can be considered effective and safe to use.
- `SN` (`Número de Serie`): the serial number. Under the EU falsified medicines framework, medicine packs are serialized to help prevent counterfeit medicines from entering the legitimate supply chain.
- `LOTE` (`Número de Lote`): the batch or lot number. It identifies a manufacturing batch so products can be traced and recalled if needed.

## The Real Problem

Spanish medicinal product boxes usually show the same information twice:

- as human-readable text printed beside the code, such as `PC`, `SN`, `Lot`, and `EXP`;
- as a machine-readable GS1 DataMatrix symbol.

The scanner reads the DataMatrix symbol, not the printed text. That symbol encodes a single GS1 payload. The payload can contain hidden control separators, especially the ASCII group separator character 29, used after variable-length fields such as lot number (`10`) and serial number (`21`).

A fully preserved scan may be conceptually like this:

```text
010847000700681721PE42EEADPA9HW4<GS>1728033110V06
```

where `<GS>` represents one hidden group separator character. It is still one string, not four printed lines.

The scanner used for the original pharmacy workflow produced flattened strings like this, and the bundled fixtures preserve that real output shape:

```text
010847000700681721PE42EEADPA9HW41728033110V06
```

That means the parser must work after the scanner-to-Excel path has already removed or hidden the separators. Now the string is ambiguous. The `17` after `PE42EEADPA9HW4` might be the expiry-date Application Identifier, or it might have been part of the serial number. The same problem can happen with `10`, `21`, or `71` inside real values.

So this project has two jobs:

1. recover likely fields from flattened scanner strings like the real fixture data;
2. parse normal GS1 strings when separators are preserved.

Recovery cannot be perfect for every possible scan. When the input is genuinely ambiguous, the parser returns `AMBIGUOUS`, `PARTIAL`, or `UNPARSED` rather than pretending certainty.

## Supported Tools

The project has two supported surfaces:

1. An Excel VBA module for pharmacy workflows where the scanner writes directly into a spreadsheet.
2. A small Python CLI for macOS/Linux/Windows validation, batch conversion, and regression tests.

The full documentation lives in `docs-site/` and is designed for GitHub Pages.

## Excel Quickstart

1. Open Excel.
2. Enable macros for the workbook.
3. Download only [`ParseEncodedString.bas`](https://raw.githubusercontent.com/mrueda/datamatrix2codes/master/macro/ParseEncodedString.bas).
4. Import `ParseEncodedString.bas` into the workbook from the VBA editor.
5. If the raw scanner code is in `A2`, use:

```excel
=ParseEncodedString(A2,"PC")
=ParseEncodedString(A2,"SN")
=ParseEncodedString(A2,"LOTE")
=ParseEncodedString(A2,"CAD")
=ParseEncodedString(A2,"STATUS")
=ParseEncodedString(A2,"CONFIDENCE")
=ParseEncodedString(A2,"HAS_GS")
=ParseEncodedString(A2,"EXPLAIN")
```

If Excel rejects the formula, use your local argument separator. Spanish/macOS Excel commonly uses semicolons, for example `=ParseEncodedString(A2;"PC")`.

`STATUS` returns:

| Status | Meaning |
| --- | --- |
| `OK` | All four target fields were parsed confidently. |
| `PARTIAL` | Some fields were missing or could not be recovered. |
| `AMBIGUOUS` | More than one valid interpretation exists; uncertain fields are blank. |
| `UNPARSED` | The scan could not be decoded into the supported fields. This does not mean the medicine code itself is invalid. |

The VBA code is pure VBA. It does not use `VBScript.RegExp`, ActiveX, or Windows-only references, so it is intended to work on both Excel for Mac and Excel for Windows.

For a full worksheet, run `DataMatrix2Codes` once before scanning. On an empty sheet it creates the headers and formats columns `A:I` as text. Then scan raw strings from `A2` downward and run `DataMatrix2Codes` again. It creates output columns, parsed values, and review colors.

Format columns `A:I` as text before scanning and conversion. Long scanner strings and parsed product codes must not be converted by Excel into numbers or scientific notation.

If Excel shows "Not trying to type a formula?", the scanner text reached Excel before the input column was prepared as text. Run `DataMatrix2Codes` on an empty sheet first, or configure the scanner to prefix scans with an apostrophe (`'`).

## Scanner Diagnostic

If a problematic scan lands in cell `A1`, check whether Excel received the hidden GS1 group separator:

```excel
=CODE(MID($A$1,ROW(A1),1))
```

Fill that formula downward for the length of the scanned string. If any row returns `29`, Excel contains the group separator and parsing should be more reliable.

If no row returns `29`, the scan is in the flattened form this project was built to handle. Recovery mode will be used. If the scanner can be configured differently, options such as GS1 mode, FNC1 transmission, group separator transmission, or replacing the group separator with visible text such as `<GS>` may improve reliability.

## Python Quickstart

Run from the repository root:

```bash
python3 -m datamatrix2codes data/codes.csv output.csv
```

The input may be either:

- one raw code per row, or
- a CSV file with a `CODE` column.

The output columns include parsed fields and review metadata:

```text
CODE,PC,SN,LOTE,CAD,STATUS,CONFIDENCE,HAS_GS,EXPLAIN
```

Run the regression tests with:

```bash
python3 -m unittest discover -s tests -v
```

## How Parsing Works

The parser first tries strict GS1 parsing. Fixed-length fields are consumed according to their official length, and variable-length fields use the ASCII group separator when the scanner provides it.

When separators are missing, the parser tries candidate boundaries for variable-length fields and scores the candidates. It prefers complete parses, valid GTIN check digits, valid expiry dates, no leftover text, and recognized healthcare/NHRN-style `71` segments. If equally good candidates disagree, disputed fields are returned blank and `STATUS` is `AMBIGUOUS`.

See:

- `docs-site/docs/installation/macos.md`
- `docs-site/docs/installation/windows.md`
- `docs-site/docs/usage/excel-feedback.md`
- `docs-site/docs/technical-details/parser.md`

## License

This project is distributed under the MIT License. See [LICENSE](LICENSE).
