# Excel Guide

The Excel workflow is the main user-facing workflow for pharmacies where a scanner writes the raw DataMatrix content into a cell.

## Import The Module

1. Open the workbook in Excel.
2. Open the Visual Basic editor.
3. Import `macro/ParseEncodedString.bas` as a standard module.
4. Save the workbook as a macro-enabled workbook (`.xlsm`).

The module is pure VBA and avoids Windows-only components such as `VBScript.RegExp`.

## Formulas

Assuming the raw scanner value is in `A2`:

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

If Excel rejects the formula, use your local argument separator. Spanish/macOS Excel commonly uses semicolons:

```excel
=ParseEncodedString(A2;"PC")
```

`CAD` is returned as `YYMM`. For example, March 2026 is `2603`.

## Suggested Columns

| Column | Formula |
| --- | --- |
| Raw code | Scanner input |
| PC | `=ParseEncodedString(A2,"PC")` |
| SN | `=ParseEncodedString(A2,"SN")` |
| LOTE | `=ParseEncodedString(A2,"LOTE")` |
| CAD | `=ParseEncodedString(A2,"CAD")` |
| STATUS | `=ParseEncodedString(A2,"STATUS")` |
| CONFIDENCE | `=ParseEncodedString(A2,"CONFIDENCE")` |
| HAS_GS | `=ParseEncodedString(A2,"HAS_GS")` |
| EXPLAIN | `=ParseEncodedString(A2,"EXPLAIN")` |

Review rows where `STATUS` is not `OK`.

Run `DataMatrix2Codes` once before scanning. It formats columns `A:I` as text, because Excel must not convert long scanner strings or parsed product codes into numbers, formulas, or scientific notation. After scanning, run `DataMatrix2Codes` again to convert the rows.

If Excel shows "Not trying to type a formula?", the scanner text reached Excel before the input column was prepared as text. Run `DataMatrix2Codes` on an empty sheet first, or configure the scanner to prefix scans with an apostrophe (`'`).

The setup macro writes parsed values into the output columns. The formulas above are available for manual cell-by-cell checks.

## Check For Hidden Separators

The scanner may send a hidden GS1 group separator into the Excel cell. Excel does not display it clearly.

If a scanned code is in `A1`, enter this formula in another column and fill it downward:

```excel
=CODE(MID($A$1,ROW(A1),1))
```

If any row returns `29`, Excel received the group separator. If no row returns `29`, the scan is in the same flattened form as the bundled fixture data and recovery mode is being used.

## Self-Test

The VBA module includes `RunDataMatrixSelfTest`.

Run it from the Visual Basic editor to validate the module against the bundled fixture examples. A passing result means the Excel implementation matches the expected parser behavior for the current test set.
