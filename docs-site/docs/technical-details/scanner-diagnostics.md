# Scanner Diagnostics

Most third-party scanners act like keyboards: they decode the DataMatrix symbol and type a string into Excel.

This includes the kind of USB/Bluetooth 2D scanners sold under brands such as Eyoyo. Brand is less important than the exact output string the scanner sends to Excel.

SEVeM publishes an official one-page scanner validation sheet for Spanish DataMatrix workflows: [Validación de escáneres para lectura de Datamatrix](https://www.sevem.es/wp-content/uploads/2020/06/SEVeM-0108.03_PruebasValidacionEscaneres_v1.0.pdf).

The main question is what string Excel actually received. Some scanner strings include ASCII character 29, the GS1 group separator. Some are plain flattened text. Both are still strings; the difference is whether an explicit boundary marker is present for variable-length fields.

## Excel Character Check

If the scan is in `A1`, fill this formula downward:

```excel
=CODE(MID($A$1,ROW(A1),1))
```

If a row returns `29`, Excel received an explicit GS1 group separator character.

If no row returns `29`, the Excel cell does not contain that separator character. The parser can still recover many rows by interpreting Application Identifiers such as `01`, `17`, `10`, and `21`, but some rows may be ambiguous.

## Scanner Settings To Look For

Scanner and barcode-app manuals may use names such as:

- GS1 mode;
- GS1 DataMatrix;
- Application Identifier parsing;
- FNC1 transmission;
- group separator transmission;
- keyboard wedge control character mapping;
- substitute group separator with visible text.

SEVeM's validation examples show the separator as visible `GS`, but note that scanner configuration may display it differently, for example as `'`, `|`, another character, or nothing visible.

This parser normalizes common visible separator forms when they appear before a GS1 Application Identifier:

- the real ASCII 29 group separator;
- `GS`, as shown in the SEVeM validation examples;
- `<GS>` and `{GS}`, which are common documentation/debug notations;
- `'` and `|`, which SEVeM mentions as possible scanner substitutions.
