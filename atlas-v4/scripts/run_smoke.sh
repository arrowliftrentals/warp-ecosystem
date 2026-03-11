#!/bin/bash
set -euo pipefail
# Quick smoke test — is Atlas alive?
# Time budget: < 10 seconds
cd "$(dirname "$0")/.."
python3 -m pytest tests/smoke/ -m smoke --timeout=10 -v
