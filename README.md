<div align="center">
  <a href="https://mrueda.github.io/datamatrix2codes/">
    <img src="docs-site/static/img/logo.png"
         width="240" alt="datamatrix2codes logo">
  </a>
  <p><em>Excel-first GS1 DataMatrix parsing for Spanish pharmacy scanner workflows</em></p>
</div>

# datamatrix2codes

**Parser for strings obtained from GS1 DataMatrix 2D barcodes on medicine boxes in Spain.**

[![Build and test](https://github.com/mrueda/datamatrix2codes/actions/workflows/build-and-test.yml/badge.svg)](https://github.com/mrueda/datamatrix2codes/actions/workflows/build-and-test.yml)
[![Documentation deploy](https://github.com/mrueda/datamatrix2codes/actions/workflows/documentation.yml/badge.svg)](https://github.com/mrueda/datamatrix2codes/actions/workflows/documentation.yml)
[![Documentation](https://img.shields.io/badge/docs-online-blue)](https://mrueda.github.io/datamatrix2codes/)
[![Python](https://img.shields.io/badge/python-%3E%3D3.10-blue.svg)](pyproject.toml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

`datamatrix2codes` helps pharmacists turn raw scanner strings from Spanish medicine packages into Excel columns such as `PC`, `SN`, `LOTE`, and `CAD`.

The important detail is that many scanners already decode the DataMatrix barcode, but then send Excel a flattened string where GS1 separators may be missing. This tool tries to recover the fields and marks uncertain rows for review instead of pretending they are certain.

## Start Here

- **Documentation:** <https://mrueda.github.io/datamatrix2codes/>
- **Excel Quick Start:** <https://mrueda.github.io/datamatrix2codes/docs/usage/excel-quickstart>
- **macOS Excel Install:** <https://mrueda.github.io/datamatrix2codes/docs/installation/macos>
- **Windows Excel Install:** <https://mrueda.github.io/datamatrix2codes/docs/installation/windows>
- **Download the Excel macro:** <https://raw.githubusercontent.com/mrueda/datamatrix2codes/master/macro/ParseEncodedString.bas>

## For Developers

```bash
python3 -m pip install -e .
python3 -m unittest discover -s tests -v
python3 -m py_compile src/datamatrix2codes/*.py tests/*.py
python3 -m datamatrix2codes data/codes.csv output.csv
```

Docs checks:

```bash
cd docs-site
npm install
npm run typecheck
npm run build
```

## Origin

I originally wrote this to help my sister, who is a pharmacist.

## License

MIT. See [LICENSE](LICENSE).
