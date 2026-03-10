# Contributing to Atlas v4

## For Coding Agents

Read `design-bible/CODING_PROTOCOL.md` before writing any code.

## Standards

- **Python:** 3.11+, ruff, mypy strict, Google-style docstrings
- **Commits:** Conventional Commits with `Co-Authored-By: Oz <oz-agent@warp.dev>`
- **Testing:** Acceptance tests gate everything (Volume 0, P11)
- **Branches:** `feat/<subsystem>` per coding agent

## Before Committing

```bash
ruff check src/ tests/
mypy src/ --strict
pytest tests/smoke/ -m smoke
```
