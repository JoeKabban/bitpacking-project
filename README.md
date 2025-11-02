# Bit Packing (SE Project 2025)

Python implementation of integer array compression with:
- Overlap bit packing (can cross 32-bit boundaries)
- No-overlap bit packing (no crossing)
- Overflow area packing (flag + index)

# Project structure

- bitpacking/ (algorithms)

- cli.py (command-line demo)

- bench.py (timings + ratios)

- tests/ (unit tests)

- report/ (report.md + report.pdf)

# Bit Packing (Python)

## How to run
```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
pip install -U pytest

# Demo (checks equal=true)
python cli.py --mode overlap --n 1000 --maxv 4095
python cli.py --mode no_overlap --n 1000 --maxv 4095
python cli.py --mode overflow --n 1000 --maxv 100000

# Tests
pytest

# Benchmark (writes results.csv)
python bench.py > results.csv
