# Atlas v4

**ATLAS** — Autonomous Technological Learning Adaptive System

A neuro-symbolic hybrid AI assistant with a 10-layer cognitive memory architecture.

## Quick Start

```bash
# Setup
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env

# Run
uvicorn atlas.api.server:app --host 127.0.0.1 --port 8000

# Test
pytest tests/smoke/ -m smoke
```

## Architecture

See `design-bible/00-system-principles.md` for the full design specification.

## Status

**Build Tier:** 0 (Foundation)
**Tests:** Smoke suite only
**MVA Progress:** 0/5

Co-Authored-By: Oz <oz-agent@warp.dev>
