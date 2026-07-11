# Python CLI Guide

The Python CLI is the reference implementation for testing and batch conversion. It is also the easiest way to debug parser behavior on macOS.

## Run

From the repository root:

```bash
python3 -m datamatrix2codes data/codes.csv output.csv
```

## Input Formats

One raw code per row:

```text
010847000654766321ANT7T3KA311726033110231853
010843523230050521TNCW7D02MD6A10V4TP1172505317128342594
```

Or a CSV with a `CODE` column:

```csv
CODE
010847000654766321ANT7T3KA311726033110231853
```

Use a different input column with:

```bash
python3 -m datamatrix2codes input.csv output.csv --column RawCode
```

## Output

The output CSV contains:

```text
CODE,PC,SN,LOTE,CAD,STATUS,CONFIDENCE,HAS_GS,EXPLAIN
```

Rows with `AMBIGUOUS`, `PARTIAL`, or `UNPARSED` should be reviewed manually.

## Tests

Run:

```bash
python3 -m unittest discover -s tests -v
```

The test fixture is intentionally small and focused on the known difficult cases where field identifiers also appear inside values.
