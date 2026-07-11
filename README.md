<div align="center">
  <a href="https://mrueda.github.io/datamatrix2codes/">
    <img src="docs-site/static/img/logo.png"
         width="260" alt="datamatrix2codes logo">
  </a>
  <p><em>Excel-first GS1 DataMatrix parsing for Spanish pharmacy scanner workflows</em></p>
</div>

# datamatrix2codes

**datamatrix2codes: parser for strings obtained from GS1 DataMatrix 2D barcodes on medicine boxes in Spain.**

[![Build and test](https://github.com/mrueda/datamatrix2codes/actions/workflows/build-and-test.yml/badge.svg)](https://github.com/mrueda/datamatrix2codes/actions/workflows/build-and-test.yml)
[![Documentation deploy](https://github.com/mrueda/datamatrix2codes/actions/workflows/documentation.yml/badge.svg)](https://github.com/mrueda/datamatrix2codes/actions/workflows/documentation.yml)
[![Documentation](https://img.shields.io/badge/docs-online-blue)](https://mrueda.github.io/datamatrix2codes/)
[![Python](https://img.shields.io/badge/python-%3E%3D3.10-blue.svg)](pyproject.toml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

`datamatrix2codes` turns raw scanner strings from Spanish medicine packages into the fields a pharmacy workflow expects in Excel:

| Field | Common pharmacy meaning | GS1 source |
| --- | --- | --- |
| `PC` | Product identifier used in the pharmacy sheet | AI `01` GTIN, normalized by removing a leading zero when present |
| `SN` | Numero de Serie / serial number | AI `21` |
| `LOTE` | Numero de Lote / batch or lot number | AI `10` |
| `CAD` | Fecha de Caducidad / expiry date as `YYMM` | AI `17` |

The primary user is a pharmacist with a third-party scanner that writes one decoded barcode string directly into Excel. The repository also includes a Python implementation for validation, batch conversion, and regression testing.

**Documentation:** <a href="https://mrueda.github.io/datamatrix2codes/" target="_blank">https://mrueda.github.io/datamatrix2codes/</a>

**Excel Quick Start:** <a href="https://mrueda.github.io/datamatrix2codes/docs/usage/excel-quickstart" target="_blank">https://mrueda.github.io/datamatrix2codes/docs/usage/excel-quickstart</a>

**macOS Excel Install:** <a href="https://mrueda.github.io/datamatrix2codes/docs/installation/macos" target="_blank">https://mrueda.github.io/datamatrix2codes/docs/installation/macos</a>

**Windows Excel Install:** <a href="https://mrueda.github.io/datamatrix2codes/docs/installation/windows" target="_blank">https://mrueda.github.io/datamatrix2codes/docs/installation/windows</a>

**Excel macro download:** <a href="https://raw.githubusercontent.com/mrueda/datamatrix2codes/master/macro/ParseEncodedString.bas" target="_blank">ParseEncodedString.bas</a>

**GitHub Actions:** <a href="https://github.com/mrueda/datamatrix2codes/actions/workflows/build-and-test.yml" target="_blank">Build and test</a> · <a href="https://github.com/mrueda/datamatrix2codes/actions/workflows/documentation.yml" target="_blank">Documentation deploy</a>

## Why This Exists

The DataMatrix symbol on a medicine box is not the same thing as the printed `PC`, `SN`, `LOTE`, and `CAD` text beside it. A scanner decodes the symbol into one GS1 payload string. That payload may contain hidden separators, especially ASCII group separator character 29, after variable-length fields.

When the scanner-to-Excel path preserves those separators, parsing is straightforward:

```text
010847000700681721PE42EEADPA9HW4<GS>1728033110V06
```

Many practical pharmacy setups do not preserve them. They send a flattened string like this instead:

```text
010847000700681721PE42EEADPA9HW41728033110V06
```

At that point the problem is no longer simply "read the barcode." The barcode has already been read. The problem is recovering field boundaries from a flattened string where values may themselves contain `17`, `10`, `21`, or `71`.

This project handles both cases:

- strict parsing when GS1 separators are present;
- recovery parsing when a scanner or Excel workflow has flattened the payload.

Recovery cannot be perfect for every possible string. When the input is incomplete or genuinely ambiguous, the tool marks the row as `PARTIAL`, `AMBIGUOUS`, or `UNPARSED` instead of inventing certainty.

## Excel Users

Most Excel users only need one file:

1. Download [`ParseEncodedString.bas`](https://raw.githubusercontent.com/mrueda/datamatrix2codes/master/macro/ParseEncodedString.bas).
2. Open Excel and enable macros for the workbook.
3. Open the VBA editor.
4. Import the `.bas` file into the workbook.
5. Scan raw codes into column `A`.
6. Run the `DataMatrix2Codes` macro to fill parsed columns and review colors.

The macro is plain VBA. It does not require Perl, Python, ActiveX, `VBScript.RegExp`, or Windows-only references. It is intended to work in Excel for macOS and Excel for Windows.

For detailed installation screenshots:

- [macOS Excel install](docs-site/docs/installation/macos.md)
- [Windows Excel install](docs-site/docs/installation/windows.md)
- [Excel quick start](docs-site/docs/usage/excel-quickstart.md)
- [Review colors](docs-site/docs/usage/review-colors.md)

## Python Users

Install from the repository root:

```bash
python3 -m pip install -e .
```

Convert one raw code per row, or a CSV file with a `CODE` column:

```bash
python3 -m datamatrix2codes data/codes.csv output.csv
```

The output columns are:

```text
CODE,PC,SN,LOTE,CAD,STATUS,CONFIDENCE,HAS_GS,EXPLAIN
```

Run the test suite:

```bash
python3 -m unittest discover -s tests -v
python3 -m py_compile datamatrix2codes/*.py tests/*.py
```

## Status Values

| Status | Meaning |
| --- | --- |
| `OK` | The target fields were parsed confidently. |
| `PARTIAL` | Some fields were found, but the row is incomplete. |
| `AMBIGUOUS` | More than one plausible interpretation exists; disputed fields are left blank for review. |
| `UNPARSED` | The string could not be decoded into the supported fields. This does not prove the medicine code itself is invalid. |

Excel uses the same statuses to color rows for review.

## Documentation Site

The Docusaurus site in `docs-site/` is the main user documentation. It includes:

- an overview for pharmacists;
- Excel installation guides for macOS and Windows;
- conversion workflow screenshots;
- example scanner strings and parsed results;
- parser notes and scanner diagnostics.

Build the docs locally with:

```bash
cd docs-site
npm install
npm run typecheck
npm run build
```

## Project Layout

| Path | Purpose |
| --- | --- |
| `macro/ParseEncodedString.bas` | Excel VBA module for pharmacists. |
| `datamatrix2codes/` | Python parser and CLI. |
| `tests/` | Regression tests, including flattened scanner strings. |
| `data/` | Fixture input and expected parsed output. |
| `docs-site/` | Docusaurus documentation site. |
| `.github/workflows/` | Python and documentation CI. |

## Origin

I originally wrote this to help my sister, who is a pharmacist. The goal is practical: make scanner-to-Excel workflows less fragile and make uncertain rows obvious enough that a pharmacist can review them.

## License

This project is distributed under the MIT License. See [LICENSE](LICENSE).
