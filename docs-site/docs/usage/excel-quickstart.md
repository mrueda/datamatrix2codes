import conversionWorkflow from '@site/static/img/excel-conversion-workflow.png';

# Excel Quick Start

:::important Before you start
Install the Excel module first. If you have not imported `ParseEncodedString.bas` into your workbook yet, follow [Install in Excel for Mac](../installation/macos.md) or [Install in Excel for Windows](../installation/windows.md).

Excel users only need the single [`ParseEncodedString.bas`](https://raw.githubusercontent.com/mrueda/datamatrix2codes/master/macro/ParseEncodedString.bas) file, not the full repository.
:::

1. Run `DataMatrix2Codes`. On an empty sheet, it prepares the scanner worksheet.
2. Scan raw strings into column `A` under the header `CODE`.
3. Run `DataMatrix2Codes` again to convert the rows.
4. Review rows where `STATUS` is not `OK`.

`DataMatrix2Codes` formats columns `A:I` as text before scanning and conversion. This matters because Excel treats some scanner input as formulas and converts long numeric-looking values such as `PC` to scientific notation unless the cells are already text.

See [Example Codes](./example-codes.md) for complete raw strings and their parsed `PC`, `SN`, `LOTE`, `CAD`, and review columns.

<figure>
  <img src={conversionWorkflow} alt="Synthetic Excel workbook showing scanner strings converted into PC, SN, LOTE, CAD, STATUS, CONFIDENCE, and EXPLAIN columns" />
  <figcaption>Synthetic conversion workflow. The scanner writes raw strings in `CODE`; the macro fills parsed columns and review messages.</figcaption>
</figure>

The macro creates this worksheet shape:

| CODE | PC | SN | LOTE | CAD | STATUS | CONFIDENCE | HAS_GS | EXPLAIN |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| raw scan | parsed | parsed | parsed | parsed | review status | 0-100 | TRUE/FALSE | short explanation |

You can also use formulas directly:

```excel
=ParseEncodedString(A2,"PC")
=ParseEncodedString(A2,"SN")
=ParseEncodedString(A2,"LOTE")
=ParseEncodedString(A2,"CAD")
=ParseEncodedString(A2,"STATUS")
=ParseEncodedString(A2,"EXPLAIN")
```

If Excel rejects the formula, use your local argument separator. Spanish/macOS Excel commonly uses semicolons:

```excel
=ParseEncodedString(A2;"PC")
```

`CAD` is returned as `YYMM`. For example, November 2028 is `2811`.
