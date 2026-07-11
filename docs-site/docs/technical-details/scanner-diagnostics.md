# Scanner Diagnostics

Most third-party scanners act like keyboards: they decode the DataMatrix symbol and type a string into Excel.

The important question is whether the scanner-to-Excel path preserves ASCII character 29, the GS1 group separator.

## Excel Character Check

If the scan is in `A1`, fill this formula downward:

```excel
=CODE(MID($A$1,ROW(A1),1))
```

If a row returns `29`, the separator reached Excel.

If no row returns `29`, the scan is flattened. The parser can still recover many rows, but some rows may be ambiguous.

## Scanner Settings To Look For

Scanner manuals may use names such as:

- GS1 mode;
- FNC1 transmission;
- group separator transmission;
- keyboard wedge control character mapping;
- substitute group separator with visible text.

If the scanner can emit `<GS>` for the group separator, this parser will normalize it automatically.
