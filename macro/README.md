# Excel Macro

`ParseEncodedString.bas` is the file to import into Excel.

Excel's VBA file browser expects files such as `.bas`, `.cls`, and `.frm`, so this repository ships the macro as `.bas`.

Excel users only need this file. They can download it directly:

<https://raw.githubusercontent.com/mrueda/datamatrix2codes/master/macro/ParseEncodedString.bas>

If the browser saves it as `ParseEncodedString.bas.txt`, rename it to `ParseEncodedString.bas`.

In the Visual Basic editor, select your workbook in Project Explorer and use **File > Import File...**. If the menu is hidden, right-click the workbook or the `Modules` folder and choose **Import File...**. Select the downloaded `ParseEncodedString.bas`.

After import, the module should appear as `DataMatrix2CodesModule`. The worksheet function remains `ParseEncodedString`.

If import is unavailable, create a new module with **Insert > Module**, open `ParseEncodedString.bas` in a text editor, and paste the code from `Option Explicit` downward. Skip the first `Attribute VB_Name = ...` line when pasting manually.

After importing, use:

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

The module is pure VBA and is intended for both Excel for Mac and Excel for Windows.

For a complete scanner worksheet, run `DataMatrix2Codes` once before scanning. On an empty sheet it creates the headers, formats columns `A:I` as text, and selects the first scanner row. Scan raw strings from `A2` downward, then run `DataMatrix2Codes` again. The macro creates parsed values and review colors.

If Excel shows "Not trying to type a formula?", the scanner text reached Excel before the input column was prepared as text. Run `DataMatrix2Codes` on an empty sheet first, or configure the scanner to prefix scans with an apostrophe (`'`).

If Excel raises a VBA error, select a raw scanner cell and run `DiagnoseDataMatrixActiveCell`. It reports the detected cell type and parser result for that cell.

For full instructions, see the Docusaurus docs under [../docs-site/docs](../docs-site/docs).
