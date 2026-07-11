# Python CLI

The Python CLI is the tested reference implementation. It is useful for batch checks, CI, and debugging outside Excel.

Run from the repository root:

```bash
python3 -m datamatrix2codes data/codes.csv output.csv
```

Input can be:

- one raw scanner string per row;
- a CSV with a `CODE` column;
- a CSV with another column selected by `--column`.

Example:

```bash
python3 -m datamatrix2codes scans.csv parsed.csv --column RawCode
```

Output columns:

```text
CODE,PC,SN,LOTE,CAD,STATUS,CONFIDENCE,HAS_GS,EXPLAIN
```

Run tests:

```bash
python3 -m unittest -v
```
