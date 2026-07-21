<div align="center">
  <a href="https://mrueda.github.io/datamatrix2codes/">
    <img src="docs-site/static/img/logo.svg"
         width="240" alt="datamatrix2codes logo">
  </a>
  <p><em>Excel-first GS1 DataMatrix parsing for Spanish pharmacy scanner workflows</em></p>
</div>

# datamatrix2codes

**Parser for strings obtained from GS1 DataMatrix 2D barcodes, often called matriz de datos in Spain, on medicine boxes.**

[![Build and test](https://github.com/mrueda/datamatrix2codes/actions/workflows/build-and-test.yml/badge.svg)](https://github.com/mrueda/datamatrix2codes/actions/workflows/build-and-test.yml)
[![Documentation deploy](https://github.com/mrueda/datamatrix2codes/actions/workflows/documentation.yml/badge.svg)](https://github.com/mrueda/datamatrix2codes/actions/workflows/documentation.yml)
[![Documentation](https://img.shields.io/badge/docs-online-blue)](https://mrueda.github.io/datamatrix2codes/)
[![Python](https://img.shields.io/badge/python-%3E%3D3.10-blue.svg)](pyproject.toml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

`datamatrix2codes` helps pharmacists turn raw scanner strings from Spanish medicine packages into Excel columns such as `PC`, `SN`, `LOTE`, and `CAD`.

A scanner or app may read the GS1 DataMatrix image and send Excel the raw decoded string. That string is not four separate values; it is a GS1 payload made of Application Identifiers such as `01`, `17`, `10`, and `21`. The hard part is interpreting that payload, especially when variable-length fields such as lot (`10`) or serial (`21`) are followed by more fields. The same digit sequences can appear inside real values, so some strings cannot be split with certainty. This tool recovers what it can and marks uncertain rows for review.

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

The repository includes a synthetic-code generator so demos and tests can use realistic scanner strings without publishing real medicine-pack serials:

```bash
python3 tools/generate_synthetic_codes.py --count 20 > synthetic-codes.csv
python3 tools/generate_synthetic_codes.py --status ambiguous --count 20 > ambiguous-codes.csv
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
