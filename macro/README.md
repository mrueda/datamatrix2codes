# How to use

In this script:

We transformed the macro into a UDF that takes two strings as inputs: encodedStr (the encoded string to be parsed) and param (the parameter to be extracted: "PC", "SN", "LOTE", or "CAD").

The function executes the respective regex pattern based on the Perl script to find each parameter in the encodedStr.

We use a Select Case statement to return the desired parameter based on the param input.

You can then use this function in your Excel worksheet like any other function, e.g., =ParseEncodedString(A1, "PC") to get the "PC" value from the string in cell A1.

Save this script in a VBA module, and you should be able to use the ParseEncodedString function as a formula in your worksheet. Adjust the regex patterns as necessary to match your data's structure.

## Notes

* It does not work in MacOs as it needs the VBScript (`VBScript.RegExp`) and other ActiveX related libraries that are not available. They work in Windows.

* We provide an example `datamatrix2codes.xlsm`.
