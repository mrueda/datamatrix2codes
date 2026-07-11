import excelFeedback from '@site/static/img/excel-status-feedback.png';

# Excel Feedback

The worksheet colors are designed for review:

| Status | Color | Meaning |
| --- | --- | --- |
| `OK` | Green | All target fields were parsed confidently. |
| `PARTIAL` | Amber | Some fields were parsed, but others are missing. |
| `AMBIGUOUS` | Orange/red | More than one plausible parse exists. Review the row. |
| `UNPARSED` | Gray/red | The tool could not map the string to the supported fields. |

`UNPARSED` does not mean the medicine code is invalid. It means this tool could not decode the string into `PC`, `SN`, `LOTE`, and `CAD`.

<figure>
  <img src={excelFeedback} alt="Synthetic Excel sheet showing green, amber, orange, and gray parser status rows" />
  <figcaption>Synthetic Excel-style feedback. No real product or serial data is shown.</figcaption>
</figure>

Use `EXPLAIN` to understand why a row needs review. For example:

```text
Some fields could not be found. Review this row.
The scan can be interpreted in more than one way. Check the medicine box.
```

## Why Ambiguous Rows Exist

An ambiguous row is not a software error. It means the scanner-to-Excel string no longer contains enough boundary information for a guaranteed answer.

For example:

```text
...21SYNTH17VALUE1728110010AD801
```

The `17` inside `SYNTH17VALUE` may be part of the serial number, while the later `17` may mark the expiry date. If the original hidden separator is missing, the software may not be able to prove the boundary from the flattened text alone.

When that happens, the row is colored for review and disputed fields are left blank.
