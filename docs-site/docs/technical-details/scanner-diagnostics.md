# Scanner Diagnostics

Most third-party scanners act like keyboards. They decode the DataMatrix symbol and type a string into Excel.

The first diagnostic question is simple:

> What exact string did Excel receive?

That string matters more than the scanner brand. A professional scanner can still be configured in a way that hides or replaces separator characters, and a lower-cost scanner can still work if it sends the expected string.

## Scanner Brands

These are examples of scanner vendors pharmacists or pharmacy IT teams may encounter:

| Vendor | Notes |
| --- | --- |
| [Eyoyo](https://www.eyoyousa.com/) | Lower-cost USB/Bluetooth 2D scanners. |
| [Zebra Technologies](https://www.zebra.com/us/en/products/scanners.html) | Professional barcode scanner lines used in retail, healthcare, logistics, and industry. |
| [Honeywell](https://automation.honeywell.com/us/en/products/productivity-solutions/barcode-scanners) | Professional barcode scanners and productivity hardware. |
| [Datalogic](https://www.datalogic.com/eng/) | Barcode readers and automatic data-capture products. |

The brand list is not a compatibility list. The important part is whether the scanner sends the GS1 DataMatrix payload in a useful form.

## SEVeM Context

[SEVeM](https://www.sevem.es/) is the Spanish Medicines Verification System. It is the national verification system used in Spain for the European falsified-medicines safety workflow.

In practice, this is the environment where pharmacies and their software verify the unique identifiers encoded on medicine packages.

That is why scanner configuration matters: a scan that looks almost correct to a person can still create verification alerts if the scanner or pharmacy software sends the wrong string.

SEVeM publishes a useful one-page scanner validation sheet:

- [Validación de escáneres para lectura de Datamatrix](https://www.sevem.es/wp-content/uploads/2020/06/SEVeM-0108.03_PruebasValidacionEscaneres_v1.0.pdf)

:::info What "GS" Means Here
In this project, `GS` means "group separator", not ordinary letters `G` and `S` inside a value. In the real encoded payload this may be ASCII character 29. Some scanners replace that hidden character with visible text such as `GS`, `<GS>`, `'`, or `|`.

If the scanner does not show any separator, the parser has to infer where variable-length fields end. That is where ambiguity comes from.
:::

## Good Versus Risky Output

Some scanner strings include ASCII character 29, the GS1 group separator. Some use a visible replacement such as `GS` or `|`. Some are plain flattened text.

All of those are strings. The difference is whether an explicit boundary marker is present for variable-length fields such as serial number (`21`) and lot (`10`).

## Excel Character Check

If the scan is in `A1`, fill this formula downward:

```excel
=CODE(MID($A$1,ROW(A1),1))
```

If a row returns `29`, Excel received an explicit GS1 group separator character.

If no row returns `29`, the Excel cell does not contain that hidden separator character. The parser can still recover many rows by interpreting Application Identifiers such as `01`, `17`, `10`, and `21`, but some rows may be ambiguous.

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

This parser normalizes common separator forms when they appear before a GS1 Application Identifier:

- the real ASCII 29 group separator;
- `GS`, as shown in the SEVeM validation examples;
- `<GS>` and `{GS}`, which are common documentation/debug notations;
- `'` and `|`, which SEVeM mentions as possible scanner substitutions.
