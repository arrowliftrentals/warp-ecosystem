#!/bin/bash
set -euo pipefail
# Run all linting and type checking
cd "$(dirname "$0")/.."
echo "=== ruff check ==="
python3 -m ruff check src/ tests/
echo "=== mypy ==="
python3 -m mypy src/ --strict
echo "=== All clean ==="
