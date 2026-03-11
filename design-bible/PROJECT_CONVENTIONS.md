# Atlas Rebuild — Project Conventions

| Field | Value |
|---|---|
| **Doc ID** | `DB-X00-001` |
| **Name** | Project Conventions |
| **Purpose** | Defines the project structure, naming conventions, coding standards, and documentation rules for the Atlas rebuild |
| **Owner** | Design Bible / Infrastructure |
| **Status** | `active` |
| **Supersedes** | N/A |
| **Superseded by** | N/A |
| **Author** | Oz |
| **Version** | v4 |
| **Created** | 2026-03-10 |
| **Last Modified** | 2026-03-10 |

---

## 1. Project Layout

The rebuild lives in a new directory, separate from the old codebase. The old `atlas/` and `console/` directories are reference-only — no agent modifies them.

```
WARP Ecosystem/
├── atlas/                         # OLD — reference only, do not modify
├── console/                       # OLD — reference only, do not modify
├── design-bible/                  # Design Bible + agent coordination
│
└── atlas-v4/                      # THE REBUILD
    ├── pyproject.toml             # Python project config (PEP 621)
    ├── README.md
    ├── CHANGELOG.md
    ├── CONTRIBUTING.md
    ├── .env.example               # Environment variable template
    ├── .gitignore
    │
    ├── src/                       # Backend (Python, src layout per PEP 517)
    │   └── atlas/                 # Top-level Python package
    │       ├── __init__.py        # Version, package metadata
    │       ├── py.typed           # PEP 561 type-checking marker
    │       │
    │       ├── shared/            # Cross-cutting concerns (no subsystem owns these)
    │       │   ├── __init__.py
    │       │   ├── errors.py      # Base error hierarchy for all subsystems
    │       │   ├── logging.py     # Structured logging configuration
    │       │   ├── config.py      # Configuration loading (env + file)
    │       │   ├── types.py       # Shared type aliases and protocols
    │       │   └── llm.py         # LLM provider abstraction (R6 model independence)
    │       │
    │       ├── memory/            # Volume 1: L1-L10 memory system
    │       │   ├── __init__.py
    │       │   ├── manager.py     # MemoryManager
    │       │   ├── schemas.py     # All memory Pydantic schemas (single file, not 15)
    │       │   ├── l1_working.py
    │       │   ├── l2_short_term.py
    │       │   ├── ...
    │       │   └── l10_vector.py
    │       │
    │       ├── orchestrator/      # Volume 2: Conversation loop, intent, response
    │       │   ├── __init__.py
    │       │   ├── engine.py      # Core conversation engine (NOT a 2800-line god object)
    │       │   ├── intent.py      # Intent parsing (symbolic + ML + LLM fallback)
    │       │   ├── response.py    # Response generation + governance integration
    │       │   └── ...
    │       │
    │       ├── learning/          # Volume 3: Active learning, corrections, retraining
    │       │   └── ...
    │       │
    │       ├── self_modify/       # Volume 4: Self-modification, sandbox
    │       │   └── ...
    │       │
    │       ├── intelligence/      # Volume 5: Amplification, reasoning, growth
    │       │   └── ...
    │       │
    │       ├── voice/             # Volume 6: TTS, STT, voice interaction
    │       │   └── ...
    │       │
    │       ├── api/               # Volume 8: Server, routes, middleware
    │       │   ├── __init__.py
    │       │   ├── server.py      # FastAPI app creation and startup
    │       │   ├── middleware.py
    │       │   └── routes/        # One file per route group
    │       │       ├── chat.py
    │       │       ├── memory.py
    │       │       ├── health.py
    │       │       └── ...
    │       │
    │       ├── governance/        # Volume 9: Validation, output governance
    │       │   ├── __init__.py
    │       │   ├── validator.py   # DecisionValidator
    │       │   ├── output.py      # GovernedOutput, AnswerGovernor
    │       │   └── schemas.py     # Governance Pydantic schemas
    │       │
    │       └── tools/             # Volume 10: Tool registry and implementations
    │           ├── __init__.py
    │           ├── registry.py    # Tool registration and lookup
    │           ├── file.py        # File operations
    │           ├── git.py         # Git operations
    │           ├── web.py         # Web search/fetch
    │           └── ...
    │
    ├── console/                   # Volume 7: Frontend (TypeScript + React)
    │   ├── package.json
    │   ├── tsconfig.json
    │   ├── vite.config.ts
    │   └── src/
    │       ├── App.tsx
    │       ├── main.tsx
    │       ├── components/        # React components (PascalCase files)
    │       │   ├── ChatPanel.tsx
    │       │   └── ...
    │       ├── lib/               # Utilities and API clients
    │       │   ├── atlasClient.ts
    │       │   └── types.ts       # Shared TypeScript types
    │       ├── pages/             # Page-level components
    │       └── contexts/          # React contexts
    │
    ├── contracts/                 # Shared API contracts (R9)
    │   ├── __init__.py
    │   ├── api_schemas.py         # Pydantic request/response models (source of truth)
    │   └── generate_ts_types.py   # Script to generate TypeScript types from Pydantic
    │
    ├── tests/                     # All tests (P11 tiered structure)
    │   ├── conftest.py            # Shared fixtures, test database setup
    │   ├── pytest.ini             # Markers: smoke, acceptance, integration, unit
    │   │
    │   ├── smoke/                 # Tier 1: < 10 seconds, "is Atlas alive?"
    │   │   ├── conftest.py
    │   │   └── test_alive.py      # Boot server, send hello, verify response
    │   │
    │   ├── acceptance/            # Tier 2: Live server, no mocks, prove it works
    │   │   ├── conftest.py        # Live server fixture
    │   │   ├── test_conversation.py
    │   │   ├── test_memory.py
    │   │   ├── test_learning.py
    │   │   └── ...                # One file per subsystem
    │   │
    │   ├── integration/           # Tier 3: Real components, no boundary mocks
    │   │   ├── memory/
    │   │   ├── orchestrator/
    │   │   ├── learning/
    │   │   └── ...                # Mirrors src/ structure
    │   │
    │   └── unit/                  # Tier 4: Isolated, mocks allowed
    │       ├── memory/
    │       ├── orchestrator/
    │       ├── learning/
    │       └── ...                # Mirrors src/ structure
    │
    ├── scripts/                   # Developer utilities
    │   ├── run_smoke.sh           # Quick smoke test runner
    │   ├── run_acceptance.sh      # Acceptance test runner (starts server first)
    │   └── generate_contracts.sh  # Regenerate TypeScript types from Pydantic
    │
    └── data/                      # Runtime data (gitignored except structure)
        ├── .gitkeep
        ├── db/                    # SQLite databases
        └── models/                # ML model files
```

### Why This Layout
- **`src/` layout (PEP 517):** Prevents accidental imports from the project root. Industry standard for modern Python packages.
- **Single `atlas` package:** All backend code lives under one importable namespace (`from atlas.memory import MemoryManager`). No confused import paths like Attempt 3.
- **`shared/` for cross-cutting:** Errors, logging, config, LLM abstraction — things every subsystem needs but no subsystem owns. Prevents the "homeless infrastructure" problem.
- **`contracts/` for R9:** Pydantic schemas are the source of truth. TypeScript types are generated from them. One change, one source.
- **Test tiers match P11:** Directory structure enforces the testing hierarchy. `pytest -m smoke` runs in 10 seconds. `pytest -m acceptance` proves the system works.

---

## 2. Naming Conventions

### Python (PEP 8, strictly enforced)

| Element | Convention | Example |
|---|---|---|
| Modules (files) | snake_case | `memory_manager.py`, `intent_parser.py` |
| Packages (dirs) | snake_case | `self_modify/`, `memory/` |
| Classes | PascalCase | `MemoryManager`, `DecisionValidator` |
| Functions/methods | snake_case | `store_fact()`, `parse_intent()` |
| Variables | snake_case | `session_id`, `confidence_score` |
| Constants | UPPER_SNAKE_CASE | `MAX_RETRIES`, `DEFAULT_PORT` |
| Private | leading underscore | `_internal_cache`, `_validate()` |
| Pydantic schemas | PascalCase, descriptive | `EpisodicEntry`, `GovernedOutput` |
| Type aliases | PascalCase | `LayerId`, `ConfidenceScore` |
| Protocols/ABCs | PascalCase with suffix | `MemoryLayer` (Protocol), `BaseTool` (ABC) |

### TypeScript / React

| Element | Convention | Example |
|---|---|---|
| Component files | PascalCase | `ChatPanel.tsx`, `MemoryView.tsx` |
| Non-component files | camelCase | `atlasClient.ts`, `voiceGovernance.ts` |
| Components | PascalCase | `<ChatPanel />`, `<MemoryView />` |
| Functions | camelCase | `sendMessage()`, `fetchHealth()` |
| Variables | camelCase | `sessionId`, `isLoading` |
| Constants | UPPER_SNAKE_CASE | `API_BASE_URL`, `WS_RECONNECT_DELAY` |
| Types/Interfaces | PascalCase | `ChatMessage`, `HealthStatus` |
| Enums | PascalCase | `ConnectionState.Connected` |
| CSS classes | kebab-case (Tailwind) | `text-primary`, `bg-surface` |

### API Endpoints

| Convention | Example |
|---|---|
| Base path | `/v1/atlas/` |
| Resource paths | kebab-case: `/v1/atlas/chat`, `/v1/memory/episodic` |
| HTTP methods | REST: GET (read), POST (create/action), PUT (replace), PATCH (update), DELETE |
| Request body | `{"query": "..."}` — snake_case keys |
| Response body | snake_case keys, consistent envelope: `{"data": ..., "meta": {...}}` |

### Files and Directories

| Context | Convention | Example |
|---|---|---|
| Python modules | snake_case | `intent_parser.py` |
| Test files | `test_` prefix + module name | `test_memory_manager.py` |
| Config files | lowercase, kebab or dot | `pyproject.toml`, `.env.example` |
| Documentation | kebab-case | `memory-layers.md`, `getting-started.md` |
| Scripts | snake_case or kebab-case | `run_smoke.sh`, `generate_contracts.sh` |

### Git

| Element | Convention | Example |
|---|---|---|
| Branch names | `type/kebab-description` | `feat/memory-l1-working`, `fix/chat-timeout` |
| Commit messages | Conventional Commits | `feat(memory): implement L1 working memory` |
| Tags | semver | `v0.1.0`, `v0.2.0` |
| Co-author | Required | `Co-Authored-By: Oz <oz-agent@warp.dev>` |

### Environment Variables

| Convention | Example |
|---|---|
| Prefix: `ATLAS_` | `ATLAS_PORT`, `ATLAS_LOG_LEVEL` |
| Provider keys: `ATLAS_<PROVIDER>_` | `ATLAS_OPENAI_API_KEY`, `ATLAS_ANTHROPIC_API_KEY` |
| Feature flags: `ATLAS_ENABLE_<FEATURE>` | `ATLAS_ENABLE_VOICE`, `ATLAS_ENABLE_LEARNING` |

---

## 3. Coding Standards

### Python

- **Version:** 3.11+ (required for modern type hints: `X | None`, `list[str]`)
- **Formatter:** Ruff (format mode) — replaces Black, faster
- **Linter:** Ruff (lint mode) — replaces flake8, isort, pylint
- **Type checker:** mypy (strict mode)
- **Dependency management:** `pyproject.toml` with `pip-tools` or `uv` for lockfile
- **Docstrings:** Google style, required on all public functions/classes
- **Line length:** 88 characters (Ruff/Black default)
- **Imports:** Sorted by Ruff. Absolute imports only (`from atlas.memory.manager import MemoryManager`, never relative)

```python
# Good: Google-style docstring with type hints
async def store_fact(
    self,
    content: str,
    source: str,
    confidence: float,
    *,
    layer: LayerId = "l4",
) -> DeclarativeFact:
    """Store a validated fact in declarative memory.

    Args:
        content: The factual statement to store.
        source: Where this fact originated (URL, user, system).
        confidence: Confidence level, 0.0-1.0.
        layer: Target memory layer. Defaults to L4 declarative.

    Returns:
        The stored fact with generated ID and timestamp.

    Raises:
        ValidationError: If content is empty or confidence out of range.
        MemoryLayerError: If the target layer is unavailable.
    """
```

### TypeScript

- **Strict mode:** `"strict": true` in tsconfig.json
- **Formatter/Linter:** ESLint + Prettier (or Biome)
- **No `any`:** Explicit types everywhere. `unknown` if truly unknown.
- **Functional components:** React components are functions, not classes
- **Named exports:** Prefer named over default exports

### Both Languages

- **No magic numbers:** Constants with names
- **No dead code:** If it's commented out, delete it. Git has history.
- **No TODO in production:** Per Volume 0 A7. Create an issue instead.
- **Error messages include context:** Not `"failed"` but `"Failed to store fact in L4: {reason}"`
- **Max file length:** 400 lines (Python), 300 lines (TypeScript). If longer, decompose.

---

## 4. Import Structure (Python)

All imports use the full package path from `atlas`:

```python
# Correct — absolute imports from the atlas package
from atlas.memory.manager import MemoryManager
from atlas.memory.schemas import EpisodicEntry
from atlas.shared.errors import ValidationError, MemoryLayerError
from atlas.shared.config import get_config
from atlas.governance.validator import DecisionValidator

# Wrong — relative imports
from .manager import MemoryManager      # No
from ..shared.errors import Error       # No
```

This ensures every file can be understood in isolation — you always know exactly where an import comes from.

---

## 5. Pydantic Schema Conventions

```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class EpisodicEntry(BaseModel):
    """A single interaction record in episodic memory (L3).

    Stored permanently. Supports temporal queries.
    """

    id: str = Field(description="Unique identifier (UUID)")
    session_id: str = Field(description="Conversation session this belongs to")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    user_input: str = Field(description="What the user said")
    atlas_response: str = Field(description="What Atlas responded")
    intent: str = Field(description="Parsed intent classification")
    confidence: float = Field(ge=0.0, le=1.0, description="Intent confidence")
    outcome: Optional[str] = Field(default=None, description="Interaction outcome if known")

    model_config = {"frozen": True}  # Immutable after creation
```

Rules:
- Every field has a `description` in `Field()`
- Constraints via `Field()` params: `ge`, `le`, `min_length`, `max_length`, `pattern`
- `model_config = {"frozen": True}` for immutable data (most memory entries)
- One `schemas.py` per subsystem, not 15+ fragmented files
- Schemas that cross subsystem boundaries live in `contracts/api_schemas.py`

---

## 6. Error Hierarchy

```python
# atlas/shared/errors.py

class AtlasError(Exception):
    """Base for all Atlas errors. Never raise bare Exception."""

class ValidationError(AtlasError):
    """Data failed Pydantic or business rule validation."""

class MemoryLayerError(AtlasError):
    """Memory layer operation failed (read, write, query)."""

class GovernanceViolation(AtlasError):
    """Action or output violated a governance rule. Blocks execution."""

class IntentParsingError(AtlasError):
    """Intent could not be determined from user input."""

class LLMProviderError(AtlasError):
    """LLM API call failed. System must degrade gracefully per R6."""

class ToolExecutionError(AtlasError):
    """Tool invocation failed."""

class SandboxError(AtlasError):
    """Sandbox execution failed."""

class ConfigurationError(AtlasError):
    """Invalid or missing configuration."""
```

Rules:
- Never `raise Exception(...)` — always a specific subclass
- Never `except: pass` — always log with context (P5)
- Error messages include what happened, what was expected, and what to do about it
- All subsystem-specific errors inherit from a subsystem base (e.g., `MemoryLayerError` for all memory errors)

---

## 7. Logging Standard

```python
# atlas/shared/logging.py
import structlog

# Structured logging — every log entry is a JSON object with context
log = structlog.get_logger()

# Usage in any module:
from atlas.shared.logging import log

log.info("fact_stored", layer="l4", fact_id="abc-123", confidence=0.85)
log.error("memory_write_failed", layer="l4", error=str(e), fact_content=content[:100])
```

Rules:
- Use `structlog` for structured JSON logging (industry standard for observability)
- Every log entry has: event name (snake_case), relevant context as kwargs
- Log levels: `debug` (development), `info` (operations), `warning` (degraded), `error` (failure), `critical` (system down)
- Never log sensitive data (API keys, passwords, user PII beyond what's needed)
- Every error log includes enough context to diagnose without reproducing

---

## 8. Configuration Loading

```python
# atlas/shared/config.py
from pydantic_settings import BaseSettings

class AtlasConfig(BaseSettings):
    """Atlas configuration. Loaded from environment variables and .env file."""

    # Server
    port: int = 8000
    host: str = "127.0.0.1"
    log_level: str = "info"

    # LLM
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    default_llm_provider: str = "openai"

    # Features (explicit opt-in, not opt-out)
    enable_voice: bool = False
    enable_learning: bool = False
    enable_self_modify: bool = False

    model_config = {"env_prefix": "ATLAS_", "env_file": ".env"}
```

Rules:
- All config through `pydantic-settings` — validated, typed, documented
- Environment variables with `ATLAS_` prefix
- Features are **off by default** and explicitly enabled — but unlike Attempt 3, features that are ON must actually work (P11 acceptance test required)
- No `config.yaml` with 50 flags. Keep it flat and simple.

---

## 9. Documentation Standard

**Every document in the project** — Design Bible volumes, ADRs, guides, plans, specs — must follow this standard. No exceptions. This enables quick scanning, accountability tracking, and prevents orphaned/stale docs.

### 9.1 Required Header

Every document begins with this metadata block immediately after the title:

```
# [Document Title]

| Field | Value |
|---|---|
| **Doc ID** | [ID per Section 9.4 scheme] |
| **Name** | [Human-readable document name] |
| **Purpose** | [One sentence: why this document exists] |
| **Owner** | [Subsystem, volume, or team that owns this doc] |
| **Status** | `draft` \| `active` \| `deprecated` \| `superseded` |
| **Supersedes** | [Doc name/path, or "N/A"] |
| **Superseded by** | [Doc name/path, or "N/A"] |
| **Author** | [Who created this document] |
| **Version** | v[N] |
| **Created** | YYYY-MM-DD |
| **Last Modified** | YYYY-MM-DD |
```

Field rules:
- **Doc ID**: Unique alphanumeric identifier per Section 9.4. Machine-sortable, grep-friendly, collision-free.
- **Name**: The canonical name. Does not need to match the filename.
- **Purpose**: One sentence max. If you can't state the purpose in one sentence, the document is trying to do too much.
- **Owner**: Maps to a Bible volume (e.g., "Volume 1: Memory System"), a subsystem (e.g., "atlas/shared"), or "Design Bible / Infrastructure" for meta-docs.
- **Status**: Only four values. `draft` = work in progress, `active` = current and authoritative, `deprecated` = kept for reference but no longer authoritative, `superseded` = replaced by another doc (must populate "Superseded by").
- **Supersedes / Superseded by**: Creates a linked chain when docs evolve. Prevents agents from reading outdated versions.
- **Author**: Use real names or agent identifiers (e.g., "Oz", "Distillation Agent V1").
- **Version**: Integer versions. Increment on every meaningful change. Formatting-only changes do not increment.
- **Created / Last Modified**: ISO 8601 date format.

### 9.2 Required Footer

Every document ends with a modification history table:

```
---

## Modification History

| Version | Date | Modified By | Summary | Laymen Summary |
|---|---|---|---|---|
| v1 | 2026-03-10 | Oz | Initial creation | Document created from scratch |
| v2 | 2026-03-10 | Oz | Added doc standard header/footer | Added tracking metadata so we know who changed what and when |
```

Column rules:
- **Version**: Matches the version in the header. One row per version.
- **Date**: When this version was created.
- **Modified By**: Who made the change. Agent identifiers are fine.
- **Summary**: Technical description of what changed. Be specific — "updated" is useless, "added B.13 Design Quality Scorecard with 9 criteria" is useful.
- **Laymen Summary**: Plain language for quick scanning by you (the user). Written so a non-programmer can understand the change in 5 seconds. "Added a scoring system so we can tell if a design is good or bad before building it" is the right level.

### 9.3 Enforcement Rules

1. **No document is created without this standard.** Agents must include the header and footer on creation, not as a separate follow-up.
2. **Every modification updates the footer.** If you change the document, you add a row. If the modification table is missing a row, the change is not considered documented.
3. **Version in header must match latest version in footer.** If they disagree, the document is non-compliant.
4. **Status transitions must be logged.** Changing status from `active` to `deprecated` requires a modification row explaining why.
5. **The VOLUME_TEMPLATE.md includes this standard.** Distillation agents producing Bible volumes must include the header/footer in their output.
6. **Existing docs are retrofitted.** All pre-existing Design Bible documents have been updated to comply as of 2026-03-10 v2.
7. **Every document has a Doc ID.** Assigned per the scheme in Section 9.4. The Doc ID is the primary key — no two documents share the same ID.

### 9.4 Document ID Scheme

Every document receives a unique alphanumeric identifier for machine-sortable searching and cross-referencing.

**Format:** `DB-VNN-SSS`

- **DB** — Fixed prefix: Design Bible. Distinguishes from future doc types.
- **V** — Volume category: `0`-`9` for Bible volumes (matching volume number), `X` for infrastructure/meta docs.
- **NN** — Volume number: `00`-`10` for Bible volumes, `00` for infrastructure.
- **SSS** — Sequential document number within that volume: `001`, `002`, etc.

**Assignment rules:**
- Each volume's primary document is always `001` (e.g., `DB-V01-001` = Volume 1 main doc).
- Supplementary docs within a volume increment: `002`, `003`, etc.
- Infrastructure docs use the `X` prefix: `DB-X00-001`, `DB-X00-002`, etc.
- IDs are permanent. If a doc is deprecated, its ID is retired — never reassigned.
- The Doc ID appears as the first field in the header metadata table.

**Current assignments:**

| Doc ID | File | Description |
|---|---|---|
| `DB-V00-001` | `00-system-principles.md` | Volume 0: System-Wide Principles |
| `DB-V01-001` | `01-memory-system.md` | Volume 1: Memory System |
| `DB-V02-001` | `02-orchestrator.md` | Volume 2: Orchestrator & Conversation Loop |
| `DB-V03-001` | `03-learning.md` | Volume 3: Learning & Adaptation |
| `DB-V04-001` | `04-self-modification.md` | Volume 4: Self-Modification & Sandbox |
| `DB-V05-001` | `05-intelligence.md` | Volume 5: Intelligence Pipeline |
| `DB-V06-001` | `06-voice-multimodal.md` | Volume 6: Voice & Multimodal |
| `DB-V07-001` | `07-console.md` | Volume 7: Console (Frontend) |
| `DB-V08-001` | `08-api-infrastructure.md` | Volume 8: API & Infrastructure |
| `DB-V09-001` | `09-governance.md` | Volume 9: Governance & Validation |
| `DB-V10-001` | `10-external-tools.md` | Volume 10: External Tools & Capabilities |
| `DB-X00-001` | `PROJECT_CONVENTIONS.md` | Project Conventions |
| `DB-X00-002` | `VOLUME_TEMPLATE.md` | Volume Template |
| `DB-X00-003` | `AGENT_COMM.md` | Agent Communication Hub |
| `DB-X00-004` | `DISTILLATION_PROTOCOL.md` | Distillation Protocol |
| `DB-X00-005` | `CODING_PROTOCOL.md` | Coding Protocol |
| `DB-TPL-001` | `prompts/distill-phase1.md` | Phase 1 Distillation Prompt Template |
| `DB-TPL-002` | `prompts/distill-phase2.md` | Phase 2 Distillation Prompt Template |
| `DB-TPL-003` | `prompts/integration-gate.md` | Integration Gate Prompt Template |
| `DB-TPL-004` | `prompts/coding-agent.md` | Coding Agent Prompt Template |

**Future doc type prefixes** (reserved, not yet in use):
- `ADR-NNN` — Architecture Decision Records
- `RFC-NNN` — Request for Comments / proposals
- `RUN-NNN` — Runbooks / operational procedures
- `DB-TPL-NNN` — Agent prompt templates (active, assigned above)

---

## 10. Metadata Strategy

Not all files benefit from the same level of tracking metadata. The full doc standard (Section 9) is designed for **design documents** — files that capture intent, decisions, and specifications that change infrequently and deliberately. Source code files change constantly, and git is purpose-built to track that.

### 10.1 File Categories and Metadata Requirements

**Full Doc Standard (Section 9 header + footer):**
- Design Bible volumes (`design-bible/*.md`)
- Infrastructure docs (`DISTILLATION_PROTOCOL.md`, `CODING_PROTOCOL.md`, etc.)
- Agent prompt templates (`design-bible/prompts/*.md`)
- Architecture Decision Records (`docs/adr/*.md`)
- Any markdown document that captures design intent or project policy

**Module Docstring Only (no header/footer):**
- Python source files (`src/**/*.py`) — require a module-level docstring stating purpose and architectural context
- Python test files (`tests/**/*.py`) — require a module-level docstring describing what is being tested
- TypeScript source files (`console/src/**/*.ts`, `*.tsx`) — require a file-level JSDoc comment

**Purpose Comment Only (one-liner):**
- Shell scripts (`scripts/*.sh`) — require `# Purpose: <description>` as the second line (after shebang)
- Configuration files (`pyproject.toml`, `tsconfig.json`, `vite.config.ts`) — no metadata required (self-documenting via structure)
- Data/placeholder files (`.gitkeep`, `.env.example`) — no metadata required

**No Metadata Required:**
- `__init__.py` files (empty or re-exports only)
- Generated files (TypeScript types from Pydantic, lockfiles)
- Binary/data files (ML models, images, databases)

### 10.2 Rationale

Git provides authoritative authorship, timestamps, and change history for all files. The full doc standard adds value only where:
1. **Design intent matters more than code diff** — a volume's modification history explains *why* a design changed, which `git log` doesn't capture well
2. **Cross-referencing is needed** — Doc IDs enable machine-searchable links between documents
3. **Agent coordination requires versioning** — distillation agents need to know which version of a spec they're working from

For source code, git + conventional commits + module docstrings provide equivalent traceability without the maintenance overhead of keeping header metadata in sync.

### 10.3 Enforcement

- The doc linter (`scripts/lint-docs.sh`) enforces Section 9 compliance on `design-bible/**/*.md`
- Ruff enforces module docstring presence on Python files (rule `D100`/`D104` when enabled)
- Code review verifies shell script purpose comments
- `__init__.py` files and generated files are exempt from all metadata requirements

---

## Modification History

| Version | Date | Modified By | Summary | Laymen Summary |
|---|---|---|---|---|
| v1 | 2026-03-10 | Oz | Initial creation — Sections 1-8: project layout, naming conventions, coding standards, imports, Pydantic schemas, error hierarchy, logging, configuration | Created the rulebook for how all code and files in the rebuild should be organized and named |
| v2 | 2026-03-10 | Oz | Added Section 9: Documentation Standard with required header/footer, modification history table, and enforcement rules; added header/footer to this document | Added a mandatory tracking system so every document has a clear owner, version history, and plain-English change log |
| v3 | 2026-03-10 | Oz | Added Section 9.4: Document ID Scheme (DB-VNN-SSS); added Doc ID as first field in header template; assigned IDs to all 14 existing documents; added enforcement rule 7 | Added a numbering system so every document has a unique machine-searchable code |
| v4 | 2026-03-10 | Oz | Added Section 10: Metadata Strategy — defines which file types get full doc standard vs. module docstrings vs. purpose comments vs. no metadata; registered DB-X00-004/005 and DB-TPL-001 through 004 in Section 9.4 ID table | Added a policy that says design docs get full tracking headers, code files just need a description at the top, and git handles the rest |
