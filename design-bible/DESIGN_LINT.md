# ATLAS Design Bible — Design Lint Specification

| Field | Value |
|---|---|
| **Doc ID** | `DB-X00-006` |
| **Name** | Design Lint Specification |
| **Purpose** | Defines machine-enforceable rules that verify code conforms to the Design Bible's intent, not just its syntax |
| **Owner** | Design Bible / Infrastructure |
| **Status** | `active` |
| **Supersedes** | N/A |
| **Superseded by** | N/A |
| **Author** | Oz |
| **Version** | v1 |
| **Created** | 2026-03-10 |
| **Last Modified** | 2026-03-10 |

---

## 1. Purpose

Ruff catches style violations. Mypy catches type violations. Pytest catches behavioral violations. **Design-lint catches design violations** — code that is technically correct but violates Volume 0 principles, boundary ownership, dependency direction, or the Design Bible's stated intent.

Design-lint answers the question: **does this code qualitatively fit the design's intended purpose, not just function correctly?**

### 1.1 Three Enforcement Layers

| Layer | What it catches | How it checks | When it activates |
|---|---|---|---|
| **Layer 1: Structural** | Wrong patterns in code | AST analysis, regex, file-structure checks | Tier 0 (from first commit) |
| **Layer 2: Architectural** | Wrong relationships between modules | Import graph, dependency direction, boundary enforcement | Tier 2 (when multiple subsystems exist) |
| **Layer 3: Semantic** | Wrong design decisions | Agent-assisted review against volume specs | Tier 3+ (when governance pipeline is live) |

Layers 1 and 2 are fully automated — they run as `python -m atlas.tools.design_lint` alongside `ruff` and `mypy` in every commit check. Layer 3 is agent-assisted and runs during PR review or self-modification proposals.

### 1.2 Severity Levels

| Severity | Meaning | Maps to |
|---|---|---|
| **BLOCK** | Merge is forbidden until resolved | Vol 0 §6 Hard Rules |
| **WARN** | Logged and flagged in PR review; does not block | Vol 0 §6 Soft Rules |
| **INFO** | Recorded for design review agent; invisible in CI | Vol 0 §6 Aspirational Rules |

---

## 2. Layer 1 Rules: Structural (AST + File-Level)

These rules analyze individual files. No cross-file context needed.

### DL-001: No Exception Swallowing
- **Source:** Volume 0 P5, A4
- **Severity:** BLOCK
- **Check:** AST scan for `except` handlers that contain only `pass`, `...`, or `continue` with no logging call. Bare `except:` (no exception type) is always blocked regardless of body.
- **Rationale:** Silent failure is a system fault. Every exception must at minimum be logged with context.

### DL-002: No TODO in Production Code
- **Source:** Volume 0 A7, PROJECT_CONVENTIONS §3
- **Severity:** BLOCK
- **Check:** Regex scan for `TODO`, `FIXME`, `HACK`, `XXX` in `src/` files. Allowed in `tests/` with a `# TODO(issue-NNN)` format linking to a tracked issue.
- **Rationale:** TODOs become permanent invisible debt. Either implement it, raise `NotImplementedError`, or create an issue.

### DL-003: No Bare Exception Raises
- **Source:** PROJECT_CONVENTIONS §6
- **Severity:** BLOCK
- **Check:** AST scan for `raise Exception(...)` or `raise BaseException(...)`. All raises must use `AtlasError` subclasses.
- **Rationale:** Generic exceptions bypass the error taxonomy and make structured error handling impossible.

### DL-004: File Length Limits
- **Source:** Volume 0 P7, A5, PROJECT_CONVENTIONS §3
- **Severity:** WARN at 400 lines, BLOCK at 600 lines (Python). WARN at 300, BLOCK at 500 (TypeScript).
- **Check:** Line count of `src/` files. Blank lines and comments count. Docstrings count.
- **Rationale:** Attempt 3's `atlas.py` reached 2800+ lines. The rebuild enforces decomposition.

### DL-005: Module Docstrings Required
- **Source:** PROJECT_CONVENTIONS §10.1
- **Severity:** WARN
- **Check:** Every `.py` file in `src/atlas/` must have a module-level docstring (first expression is a string literal).
- **Rationale:** Every file must state its purpose and architectural context so any agent can understand it in isolation.

### DL-006: Public Functions Require Type Hints
- **Source:** CODING_PROTOCOL §3.4, PROJECT_CONVENTIONS §3
- **Severity:** BLOCK
- **Check:** AST scan for function definitions in `src/` that lack return type annotations or have untyped parameters (excluding `self`, `cls`).
- **Rationale:** Type hints are the foundation of static analysis. Mypy enforces correctness; this enforces presence.

### DL-007: Pydantic Fields Require Descriptions
- **Source:** PROJECT_CONVENTIONS §5
- **Severity:** WARN
- **Check:** AST scan for `Field()` calls in Pydantic models that lack a `description` keyword argument. Fields with no `Field()` wrapper (bare type annotation) in models within `schemas.py` files are flagged.
- **Rationale:** Schema descriptions are documentation that travels with the data. They enable auto-generated API docs and agent comprehension.

### DL-008: No Simulated Capabilities
- **Source:** Volume 0 A3
- **Severity:** BLOCK
- **Check:** AST scan for `hashlib.md5` usage outside of test files and integrity-checking modules (`integrity.py`, `verification.py`). Scan for functions that return hardcoded fake data when the function name implies real computation (heuristic: function contains `detect`, `analyze`, `classify`, `predict` and body is `return None` or `return {}` or `return False`).
- **Rationale:** If a capability isn't real, it must say so. No fake results dressed up as real ones.

### DL-009: Health Checks Must Verify Functionality
- **Source:** Volume 0 R5, A2
- **Severity:** WARN
- **Check:** AST scan of functions named `health_check`, `get_health`, `is_healthy` or decorated with health-check markers. Flag any that return a hardcoded `True`, `"healthy"`, or `{"status": "ok"}` without calling at least one subsystem method.
- **Rationale:** Health checks must verify behavior, not just that an object was instantiated.

### DL-010: No NotImplementedError Without Feature Flag
- **Source:** Volume 0 A7, R5
- **Severity:** WARN
- **Check:** AST scan for `raise NotImplementedError` in `src/` production code. Allowed only if the containing module's `__init__` or the function has a documented feature flag reference (`ATLAS_ENABLE_*`). If the feature flag is enabled, `NotImplementedError` is a BLOCK.
- **Rationale:** Stubs are acceptable for deferred features, but only if they're gated and self-documenting.

---

## 3. Layer 2 Rules: Architectural (Cross-File)

These rules analyze relationships between files. Require building an import graph.

### DL-101: Absolute Imports Only
- **Source:** PROJECT_CONVENTIONS §4
- **Severity:** BLOCK
- **Check:** AST scan for `from .` or `from ..` relative imports in `src/atlas/`.
- **Rationale:** Relative imports make files unreadable in isolation. Every import must show its full origin.

### DL-102: Dependency Direction Enforcement
- **Source:** Volume 0 §13, build-order-refined.md
- **Severity:** BLOCK
- **Check:** Build the import graph for `src/atlas/`. Verify that imports only flow downward or laterally per the tier dependency DAG:
  - `shared/` → imported by everything, imports nothing in `atlas/`
  - `memory/` → imports only `shared/`
  - `governance/` → imports only `shared/`, `memory/` (for schemas)
  - `orchestrator/` → imports `shared/`, `memory/`, `governance/`, `tools/`
  - `learning/` → imports `shared/`, `memory/`, `governance/`
  - `self_modify/` → imports `shared/`, `memory/`, `governance/`, `learning/`
  - `intelligence/` → imports `shared/`, `memory/`
  - `voice/` → imports `shared/`, `governance/`
  - `tools/` → imports `shared/`, `memory/`, `governance/`
  - `api/` → imports everything (it's the entry point)
  - `contracts/` → imports only `shared/`

  Illegal: `memory/` importing from `orchestrator/`, `governance/` importing from `learning/`, etc.
- **Rationale:** Dependency direction enforcement prevents circular dependencies, ensures lower-tier modules remain independently testable, and makes the build order physically real (not aspirational).

### DL-103: No Direct LLM Provider Imports
- **Source:** Volume 0 R6 (Model Independence)
- **Severity:** BLOCK
- **Check:** Scan imports for `openai`, `anthropic`, `cohere`, `google.generativeai`, or any known LLM SDK package. Only `shared/llm.py` may import these. All other modules must use the `LLMProvider` Protocol from `shared/types.py`.
- **Rationale:** Atlas must work without any specific LLM. If OpenAI is down, Atlas still functions (with reduced quality).

### DL-104: Memory Layer Isolation
- **Source:** Volume 0 P6, §6 Hard Rule 3
- **Severity:** BLOCK
- **Check:** Scan for imports of `l1_working`, `l2_short_term`, ..., `l10_vector` from any module outside `memory/`. All external access must go through `MemoryManager`. Exception: `tests/` may import layer implementations for unit testing.
- **Rationale:** No layer bypasses the MemoryManager. No layer assumes authority outside its mandate.

### DL-105: Volume Ownership Boundaries
- **Source:** AGENT_COMM.md ownership claims, agent-comm/vol-*.md
- **Severity:** WARN
- **Check:** Each module in `src/atlas/<subsystem>/` is mapped to its owning volume. Cross-subsystem imports that are not declared in the consuming volume's `agent-comm/vol-XX.md` dependency declarations are flagged. The rule reads per-volume agent-comm files and builds an allowed-dependency matrix.
- **Rationale:** If a volume didn't declare a dependency, the import is either unauthorized or the dependency declaration is missing. Either way, it needs human review.

### DL-106: No Orphan Modules
- **Source:** Volume 0 P3, A1
- **Severity:** WARN
- **Check:** Build the full import graph. Flag any module in `src/atlas/` that is never imported by any other module (excluding `__init__.py` re-exports and `api/routes/` which are loaded by the server). Flag any module that has no corresponding test file in `tests/`.
- **Rationale:** A component that passes unit tests but has never been called by another component is not done (P3). This catches the Feature Factory anti-pattern.

### DL-107: Schema at Every Boundary
- **Source:** Volume 0 P8, §6 Hard Rule 1
- **Severity:** WARN
- **Check:** For every public function in a subsystem's `__init__.py` or exported interface:
  - Parameters that are `dict`, `Any`, `list`, or `tuple` without Pydantic wrapping are flagged.
  - Return types that are `dict`, `Any`, `list`, or `tuple` without Pydantic wrapping are flagged.
  - Exception: Internal helper functions (prefixed `_`) are exempt.
- **Rationale:** All data crossing subsystem boundaries must pass Pydantic validation. Raw dicts at interfaces are schema bypass.

### DL-108: Acceptance Test Exists Per Subsystem
- **Source:** Volume 0 P11, R10, A8
- **Severity:** BLOCK (after Tier 2)
- **Check:** For each directory in `src/atlas/` (memory, orchestrator, etc.), verify that at least one test file exists in `tests/acceptance/` that imports or references that subsystem. The test file must contain at least one function making an HTTP request (detected by imports of `httpx`, `requests`, `TestClient`, or `AsyncClient`).
- **Rationale:** No subsystem is done until its acceptance test passes against the live system.

---

## 4. Layer 3 Rules: Semantic (Agent-Assisted)

These rules cannot be fully automated. They are evaluated by a **Design Review Agent** that reads the relevant volume and the code diff, then produces a structured compliance report.

The Design Review Agent runs during:
- PR review (before merge)
- Self-modification proposals (Vol 4 pipeline, before `RiskAssessor`)
- Periodic audit (nightly, against the full codebase)

### DL-201: B.4 KILL Decisions Respected
- **Input:** The volume's B.4 triage table, the file list in the current diff
- **Check:** If any file or class name in the diff corresponds to a component marked KILL in B.4, flag it. Resurrecting killed components requires a documented justification in the PR.
- **Question the agent answers:** "Does this code reintroduce anything the design explicitly killed?"

### DL-202: B.3 Interface Contract Conformance
- **Input:** The volume's B.3 interface contracts, the implementation code
- **Check:** Verify that public class signatures, method signatures, and return types match what B.3 specifies. Flag deviations. Deviations are allowed only if documented in the PR as a contract change request.
- **Question:** "Does this implementation match the specified interface?"

### DL-203: B.1 Purpose Alignment
- **Input:** The volume's B.1 subsystem purpose statement, the implementation code
- **Check:** Verify that the module's functionality aligns with the stated purpose. Flag functionality that belongs to a different volume (e.g., governance logic in a memory module).
- **Question:** "Does this code do what this subsystem is supposed to do, and nothing else?"

### DL-204: Volume 0 Principle Compliance
- **Input:** All 11 principles (P1-P11), the implementation code
- **Check:** For each principle, evaluate whether the code complies. Cite specific principle IDs in violations. Priority checks:
  - P1: Is there any code path where LLM output is executed without symbolic validation?
  - P5: Are there error paths that don't log?
  - P8: Are there boundary-crossing functions without Pydantic schemas?
  - P9: Are there LLM response paths that bypass governance?
- **Question:** "Does this code violate any Volume 0 principle? Cite which one."

### DL-205: Undeclared Dependency Introduction
- **Input:** The volume's agent-comm file, the import statements in the diff
- **Check:** If the code introduces imports from a subsystem not listed in the volume's dependency declarations, flag it and require either a declaration update or a justification.
- **Question:** "Does this code introduce cross-volume dependencies that weren't declared?"

### DL-206: Error Handling Completeness
- **Input:** The volume's B.7 error handling specification, the implementation code
- **Check:** Verify that error types from B.7 are implemented and used. Verify that error propagation matches the specified strategy (raise vs. catch-and-log vs. degrade).
- **Question:** "Does this code handle errors the way the design says it should?"

---

## 5. Implementation Plan

### 5.1 Module Location
`atlas-v4/src/atlas/tools/design_lint.py` (or `design_lint/` if multiple files needed)

The linter is a tool — it lives in the tools subsystem but is invoked during development, not at runtime. It has no runtime dependencies on the Atlas server.

### 5.2 Data Sources

| Data | Source | Used by |
|---|---|---|
| Python AST | `ast.parse()` from stdlib | Layer 1, Layer 2 |
| Import graph | Walk all `src/atlas/**/*.py`, extract `import` / `from X import` | Layer 2 |
| Volume ownership map | Parse `design-bible/agent-comm/vol-*.md` for CLAIM blocks | DL-105 |
| Dependency matrix | Parse `design-bible/agent-comm/vol-*.md` for DEPENDENCY blocks | DL-105, DL-205 |
| B.4 triage tables | Parse volume `.md` files for REBUILD/DEFER/KILL verdicts | DL-201 |
| B.3 contracts | Parse volume `.md` files for interface signatures | DL-202 |
| Tier dependency DAG | Hardcoded from build-order-refined.md | DL-102 |

### 5.3 CLI Interface

```
# Run all Layer 1 + Layer 2 rules
python -m atlas.tools.design_lint check src/

# Run a specific rule
python -m atlas.tools.design_lint check src/ --rule DL-102

# Run only BLOCK-severity rules (for CI gating)
python -m atlas.tools.design_lint check src/ --severity block

# Output as JSON (for tooling integration)
python -m atlas.tools.design_lint check src/ --format json

# Lint a single file
python -m atlas.tools.design_lint check src/atlas/memory/manager.py
```

### 5.4 Output Format

```
src/atlas/memory/l3_episodic.py:45: DL-001 BLOCK — except handler swallows error without logging (P5)
src/atlas/orchestrator/engine.py:12: DL-103 BLOCK — imports 'openai' directly; must use shared/llm.py (R6)
src/atlas/tools/file.py:220: DL-004 WARN — file is 412 lines; limit is 400 (P7)
src/atlas/voice/controller.py:8: DL-105 WARN — imports from 'atlas.learning'; not declared in agent-comm/vol-06.md

4 issues (2 BLOCK, 2 WARN)
```

Every violation cites:
1. File and line number
2. Rule ID
3. Severity
4. Description
5. Source principle (parenthetical)

### 5.5 Activation Schedule

| Tier | Rules active |
|---|---|
| Tier 0 | DL-001 through DL-010 (Layer 1) + DL-101, DL-103 |
| Tier 1 | + DL-102, DL-104 |
| Tier 2 | + DL-105, DL-106, DL-107, DL-108 (all Layer 2) |
| Tier 3+ | + DL-201 through DL-206 (Layer 3 — agent-assisted, runs in PR review) |

### 5.6 Integration Points

| Context | What runs | Who invokes |
|---|---|---|
| `ruff` + `mypy` + `design-lint` | All Layer 1 + 2 rules | CODING_PROTOCOL §3.5 — before every commit |
| PR review | All Layer 1 + 2 + 3 rules | CI pipeline + Design Review Agent |
| Self-modification proposal | Layer 3 DL-201 through DL-206 | Vol 4 `SelfModifier.propose_improvement()` pipeline, before `RiskAssessor` |
| Nightly audit | Full codebase scan, all layers | Scheduled job |

---

## 6. Relationship to Existing Tools

Design-lint does NOT replace existing tools. It complements them:

| Tool | What it checks | Design-lint gap it can't cover |
|---|---|---|
| **ruff** | Style, formatting, basic lint rules | Design intent, boundary enforcement |
| **mypy** | Type correctness | Architectural direction, ownership |
| **pytest** | Behavioral correctness | Design fidelity, purpose alignment |
| **design-lint** | Design conformance | — (this is the gap filler) |

The CI pipeline runs all four in sequence. All four must pass for a merge.

---

## 7. Governance of the Linter Itself

The design-lint rules are themselves governed:
- **Adding a rule** requires citing a Volume 0 principle, Design Bible section, or a specific failure that demands it (P2: governance enables, not blocks).
- **Removing a rule** requires documenting why (what changed that makes the rule unnecessary).
- **Rule changes** are tracked in this document's modification history.
- **False positive rate** is monitored. If a rule produces >10% false positives, it must be refined or downgraded from BLOCK to WARN.
- **The linter has its own tests.** Each rule has at least one positive case (code that violates) and one negative case (code that complies). These live in `tests/unit/tools/test_design_lint.py`.

---

## Modification History

| Version | Date | Modified By | Summary | Laymen Summary |
|---|---|---|---|---|
| v1 | 2026-03-10 | Oz | Initial creation — 10 Layer 1 rules (structural/AST), 8 Layer 2 rules (architectural/import-graph), 6 Layer 3 rules (semantic/agent-assisted), implementation plan with CLI interface, activation schedule, and governance of the linter itself | Created the rulebook for a tool that checks if code matches the design intent, not just whether it compiles |
