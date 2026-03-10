#!/bin/bash
set -euo pipefail
# Acceptance tests — prove the system works end-to-end
# Time budget: < 5 minutes
cd "$(dirname "$0")/.."
python3 -m pytest tests/acceptance/ -m acceptance --timeout=30 -v
