# ATLAS Design Bible — Coding Agent Protocol

| Field | Value |
|---|---|
| **Doc ID** | `DB-X00-005` |
| **Name** | Coding Agent Protocol |
| **Purpose** | Defines operating rules, work boundaries, verification requirements, and commit protocol for coding agents building Atlas v4 |
| **Owner** | Design Bible / Infrastructure |
| **Status** | `active` |
| **Supersedes** | N/A |
| **Superseded by** | N/A |
| **Author** | Oz |
| **Version** | v1 |
| **Created** | 2026-03-10 |
| **Last Modified** | 2026-03-10 |

---

## 1. Scope

This protocol governs all agents that write production code for Atlas v4. It does NOT apply to distillation agents (see `DISTILLATION_PROTOCOL.md`).

---

## 2. Input: What Coding Agents Read

A coding agent reads ONLY these documents. Nothing else.

| Document | Purpose |
|---|---|
| `design-bible/00-system-principles.md` (Volume 0) | Binding principles, anti-patterns, requirements |
| Their assigned volume's completed Part B | Subsystem design specification |
| `design-bible/PROJECT_CONVENTIONS.md` | Code standards, naming, imports, error hierarchy |
| `design-bible/CODING_PROTOCOL.md` (this file) | Operating rules |
| `design-bible/gate-output/shared-contracts.md` | Binding interface contracts |
| `atlas-v4/src/atlas/shared/` | Shared foundation code |
| Existing code in `atlas-v4/` for their dependencies | Per build order |

**Coding agents do NOT read:**
- The old `atlas/` directory (Attempt 3 source)
- Other volumes (except Volume 0)
- Old documentation in `atlas/docs/`

---

## 3. Work Rules

### 3.1 One Subsystem Per Agent
Each coding agent implements exactly one subsystem. No cross-subsystem edits without declaring a dependency in `AGENT_COMM.md`.

### 3.2 Feature Branch
Agent creates a feature branch: `feat/<subsystem>` (e.g., `feat/memory`, `feat/orchestrator`).

### 3.3 Code Location
All production code goes in `atlas-v4/src/atlas/<subsystem>/`. Tests go in `atlas-v4/tests/` following the tier structure.

### 3.4 Quality Requirements
All code must satisfy:
- Type hints on every function (Python 3.11+ syntax: `X | None`, `list[str]`)
- Google-style docstrings with Args/Returns/Raises on all public functions
- Pydantic schemas for all data types (from the volume's B.6)
- Error classes inheriting from `AtlasError` hierarchy (from the volume's B.7)
- No TODO comments — create tracked issues instead
- Max 400 lines per file — decompose if longer
- Absolute imports only: `from atlas.memory.manager import MemoryManager`

### 3.5 Tool Checks Before Commit
All code must pass:
1. `ruff check src/ tests/` — 0 errors
2. `mypy src/ --strict` — 0 errors
3. `pytest tests/smoke/ -m smoke` — all pass
4. `pytest tests/ -k <subsystem>` — all pass

Do not commit if any check fails.

---

## 4. Testing Requirements

Write tests in this order (from the volume's B.8):

### 4.1 Acceptance Tests (MANDATORY)
Location: `tests/acceptance/`
- Run against the live server (no mocks)
- Prove the subsystem works end-to-end
- Would FAIL if the implementation were deleted

At least one acceptance test per subsystem. This is non-negotiable (Volume 0 R10).

### 4.2 Integration Tests
Location: `tests/integration/<subsystem>/`
- Test real component interactions
- No mocks at subsystem boundaries
- Use real (test) databases

### 4.3 Unit Tests
Location: `tests/unit/<subsystem>/`
- Isolated function tests
- Mocks allowed
- For development speed, not deployment gating

### 4.4 Regression Tests
Location: `tests/unit/<subsystem>/`
- From the volume's B.8.4
- Test cases that would have caught Attempt 3 failures

---

## 5. Cross-Subsystem Dependencies

If a coding agent needs functionality from a subsystem that isn't built yet:

1. Check `design-bible/gate-output/shared-contracts.md` for the interface contract
2. Code against the contract interface (Protocol or ABC)
3. Create a stub implementation in `tests/stubs/` (NOT in production code)
4. When the real implementation lands, remove the stub and wire the real one
5. Declare the dependency in `AGENT_COMM.md`

---

## 6. Commit Protocol

### 6.1 Format
Conventional Commits with scope:
```
<type>(<scope>): <subject>

<body>

Co-Authored-By: Oz <oz-agent@warp.dev>
```

**Types:** feat, fix, docs, test, refactor, chore, perf
**Scope:** The subsystem name (memory, orchestrator, learning, etc.)
**Subject:** Imperative mood, no period, max 72 chars

### 6.2 Rules
- **Co-author line is mandatory** — every commit
- **Atomic commits** — one logical change per commit
- **Never commit failing tests** — all checks must pass first
- **Never commit TODO comments** — create an issue instead

---

## 7. Integration and PR

When a subsystem is complete:

1. All tests pass (smoke + subsystem acceptance + unit + integration)
2. ruff + mypy clean
3. The relevant MVA tier test must pass (from Volume 0 Section 13)
4. Agent creates a PR from `feat/<subsystem>` to the main development branch
5. PR description includes: what was built, which MVA tests pass, and any known limitations

---

## 8. Build Tier Gates

Coding agents must respect the build order (Volume 0 Section 13). Each tier has an MVA gate:

| Tier | Subsystem | MVA Gate |
|---|---|---|
| 0 | shared/ (foundation) | None — ruff + mypy pass |
| 1 | api/server + governance/validator | Server boots, /health returns 200 |
| 2 | orchestrator/ (core loop) | MVA-1: hello → coherent response |
| 3 | memory/ (all layers) | MVA-3: memory round-trip |
| 4 | governance/output | MVA-2: evidence-grounded response |
| 5 | learning/ | MVA-4: learning round-trip |
| 6+ | self_modify, intelligence, voice, tools, console | No additional MVA gates |

A tier's gate must pass before the next tier begins. This prevents Attempt 3's pattern of building everything before proving anything works.

---

## Modification History

| Version | Date | Modified By | Summary | Laymen Summary |
|---|---|---|---|---|
| v1 | 2026-03-10 | Oz | Initial creation — defined input rules, work boundaries, quality requirements, testing requirements, cross-subsystem dependency protocol, commit format, and build tier gates | Created the rulebook for coding agents that tells them exactly how to write, test, and commit code for Atlas v4 |
