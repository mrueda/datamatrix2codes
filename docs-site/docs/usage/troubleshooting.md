# Troubleshooting

## Excel Shows `#NAME?`

The VBA module is not imported, macros are disabled, or the workbook was not saved as `.xlsm`.

Check these points:

- The imported standard module should appear under `Modules` as `DataMatrix2CodesModule`.
- The workbook must be saved as `.xlsm`.
- Macros must be enabled for that workbook.
- If you imported an older copy, remove the old module and import the current `macro/ParseEncodedString.bas` again.

You do not need formulas for the normal workflow. Run `DataMatrix2Codes`; it writes parsed values directly into the sheet.

## Excel Shows Run-Time Error `13`

Run-time error `13` means VBA received a value whose type did not match what the macro expected.

Use the current `macro/ParseEncodedString.bas` file. If your workbook already has an older imported module, remove that old `ParseEncodedString` module from the Visual Basic editor and import the new `.bas` file again.

Also format columns `A:I` as **Text** before scanning and conversion. If Excel turns a long scanner string or parsed `PC` into a number or scientific notation, the original text display may be damaged.

If the error continues, select one raw scanner cell and run `DiagnoseDataMatrixActiveCell` from the Macros dialog. The diagnostic reports the cell type, detected text length, parser status, and explanation.

## Excel Asks "Not Trying To Type A Formula?"

Excel may show this when a manually typed formula uses the wrong argument separator for your regional settings.

Try semicolons instead of commas:

```excel
=ParseEncodedString(A2;"PC")
```

instead of:

```excel
=ParseEncodedString(A2,"PC")
```

This is common in Spanish/macOS Excel.

Excel can also show a similar warning if a scanner sends text beginning with `=` or `-` into a normal cell. In that case, Excel tries to interpret the scanner output as a formula before this parser can run.

Run `DataMatrix2Codes` on an empty sheet before scanning. It formats columns `A:I` as text and selects the first scanner row. After scanning, run `DataMatrix2Codes` again to convert the rows.

If your scanner can be configured with a prefix, configure it to send an apostrophe (`'`) before the barcode string. Excel stores the rest as text and does not show the apostrophe in the cell.

## Rows Are Not Colored

Run `SetupDataMatrixWorksheet` after scanning or pasting codes. The macro writes parsed values and applies conditional formatting to the active sheet.

## A Field Is Blank

Check `STATUS` and `EXPLAIN`.

- `PARTIAL`: the parser found some fields but not all.
- `AMBIGUOUS`: the scan can be interpreted in more than one way.
- `UNPARSED`: the scan could not be decoded into the supported fields.

## Check For Hidden GS1 Separators

If a scan is in `A1`, fill this formula downward:

```excel
=CODE(MID($A$1,ROW(A1),1))
```

A result of `29` means Excel received the hidden GS1 group separator. If no row returns `29`, the scan is in the flattened form this project is designed to recover from.
