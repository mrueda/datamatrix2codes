import macosInstall from '@site/static/img/macos-vba-install.png';

# Install In Excel For Mac

Use this path when the scanner writes directly into Microsoft Excel on macOS.

## Requirements

- Microsoft Excel for Mac with macros enabled.
- The single VBA module file: [`ParseEncodedString.bas`](https://raw.githubusercontent.com/mrueda/datamatrix2codes/master/macro/ParseEncodedString.bas).
- A macro-enabled workbook (`.xlsm`).

No ActiveX component is required. The module is pure VBA and does not use `VBScript.RegExp`.

Use `ParseEncodedString.bas` for import. Excel's VBA file browser expects `.bas` for standard modules.

You do not need to download the full repository for Excel use. Download only [`ParseEncodedString.bas`](https://raw.githubusercontent.com/mrueda/datamatrix2codes/master/macro/ParseEncodedString.bas). If your browser saves it as `ParseEncodedString.bas.txt`, rename it to `ParseEncodedString.bas` before importing.

## Import The VBA Module

1. Open Excel.
2. Create or open the workbook where the scanner will write codes.
3. Save it as an Excel Macro-Enabled Workbook (`.xlsm`).
4. Download [`ParseEncodedString.bas`](https://raw.githubusercontent.com/mrueda/datamatrix2codes/master/macro/ParseEncodedString.bas).
5. Open the Visual Basic editor from **Tools > Macro > Visual Basic Editor**. On some Macs this is also available from **Developer > Visual Basic**.
6. Open Project Explorer with **View > Project Explorer** if the project tree is not visible.
7. In Project Explorer, select `VBAProject (your-workbook-name.xlsm)`.
8. Use **File > Import File...** and select the downloaded `ParseEncodedString.bas`.
9. If you do not see **Import File...**, right-click the workbook project or the `Modules` folder in Project Explorer and choose **Import File...**.
10. Confirm that a module named `DataMatrix2CodesModule` appears under `Modules`.
11. Save the workbook again.

<figure>
  <img src={macosInstall} alt="Synthetic macOS Excel workbook showing imported VBA module and status-colored scanner results" />
  <figcaption>Synthetic macOS Excel setup. No real product or serial data is shown.</figcaption>
</figure>

## Next Step

After the module is imported, follow [Excel Quick Start](../usage/excel-quickstart.md). That page covers the scanner workflow, including when to run `DataMatrix2Codes`.

## If Import Is Still Hidden

Use the manual fallback:

1. In the Visual Basic editor, use **Insert > Module**.
2. Open `macro/ParseEncodedString.bas` in a text editor.
3. Copy the code from `Option Explicit` downward into the new module. Skip the first `Attribute VB_Name = ...` line when pasting manually.
4. Save the workbook as `.xlsm`.

## Validate The Module

Run `RunDataMatrixSelfTest` from the Visual Basic editor. It checks the bundled fixture cases and reports whether the VBA parser matches the expected behavior.

## macOS Macro Security

If Excel blocks macros, open Excel settings and allow macros for this workbook. Keep the workbook in a trusted folder if your organization requires it.
