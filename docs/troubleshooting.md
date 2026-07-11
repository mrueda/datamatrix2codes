# Troubleshooting

## Excel Shows `#NAME?`

The VBA module is not imported, macros are disabled, or the workbook was not saved as `.xlsm`.

Check these points:

- The imported standard module should appear under `Modules` as `DataMatrix2CodesModule`.
- The workbook must be saved as `.xlsm`.
- Macros must be enabled for that workbook.
- If you imported an older copy, remove the old module and import the current `macro/ParseEncodedString.bas` again.

You do not need formulas for the normal workflow. Run `DataMatrix2Codes`; it writes parsed values directly into the sheet.

## Excel On Mac Does Not Run The Macro

Check macro security settings and make sure the module was imported as a standard module. The parser does not require Windows-only ActiveX components.

## Excel Shows Run-Time Error `13`

Run-time error `13` means VBA received a value whose type did not match what the macro expected.

Use the current `macro/ParseEncodedString.bas` file. If your workbook already has an older imported module, remove that old `ParseEncodedString` module from the Visual Basic editor and import the new `.bas` file again.

Also format columns `A:I` as text before scanning and conversion. Excel must not convert long scanner strings or parsed product codes into numbers or scientific notation.

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

## A Field Is Blank

Blank fields mean the parser could not identify that value confidently. Check `STATUS`:

- `PARTIAL`: the field was missing or the parser could not recover it.
- `AMBIGUOUS`: more than one valid interpretation exists.
- `UNPARSED`: the scan could not be decoded into the supported fields. This does not mean the medicine code itself is invalid.

## Scanner Output Contains Strange Separators

GS1 variable-length fields may be separated by ASCII character 29. Some scanners show this as an invisible character, while others can be configured to output visible text.

The parser accepts:

- the real ASCII character 29;
- `<GS>`;
- `{GS}`.

The parser is designed to handle flattened scanner output like the bundled fixtures. If possible, configure the scanner to preserve or emit a visible group separator anyway; that makes parsing more reliable.

To check one scan in Excel, put the raw scan in `A1` and fill this formula downward:

```excel
=CODE(MID($A$1,ROW(A1),1))
```

A result of `29` means the hidden separator reached Excel.

## Python Cannot Find The Module

Run commands from the repository root:

```bash
python3 -m datamatrix2codes data/codes.csv output.csv
```

For tests:

```bash
python3 -m unittest discover -s tests -v
```
