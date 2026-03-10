# Design Bible Volume Template

| Field | Value |
|---|---|
| **Doc ID** | `DB-X00-002` |
| **Name** | Volume Template |
| **Purpose** | Defines the mandatory structure every distillation agent must follow when producing a per-subsystem Bible volume |
| **Owner** | Design Bible / Infrastructure |
| **Status** | `active` |
| **Supersedes** | N/A |
| **Superseded by** | N/A |
| **Author** | Oz |
| **Version** | v4 |
| **Created** | 2026-03-10 |
| **Last Modified** | 2026-03-10 |

Each volume has two parts:

- **Part A: Context** — Pre-loaded by the orchestrating agent. Contains the source manifest (what to read), a context brief (what's already known), and known failures. The distillation agent reads this BEFORE diving into old code/docs.
- **Part B: Design Specification** — Filled out by the distillation agent AFTER reading all sources listed in Part A. This is the output that programming agents will use to build the new system.

**Rules for distillation agents:**
1. Read Volume 0 (`00-system-principles.md`) first. All principles, anti-patterns, and requirements there are binding.
2. Read everything in the Part A source manifest. Do not skip files.
3. Fill out every section in Part B. If a section is not applicable, write "N/A — [reason]".
4. Do not copy code from old sources. Describe design intent, interface contracts, and behavior. The programming agent writes fresh code.
5. If you discover design decisions not captured in Volume 0, flag them in Section B.10.
6. Be specific. "Memory layer should persist data" is useless. "L3 Episodic stores interaction records in SQLite with columns: id, session_id, timestamp, user_input, atlas_response, intent, confidence, outcome" is useful.
7. For scope triage (Section B.4), every component in the source manifest must get a verdict. No omissions.

---

## Part A: Context (Pre-loaded)

### A.1 Subsystem Identity
- **Volume number and title**
- **One-sentence purpose**: What does this subsystem do for Atlas?
- **Rebuild phase**: When in the build order does this get built? (from Volume 0, Section 11)

### A.2 Source Manifest
**Code files to read** (paths relative to `atlas/`):

Each file must be tagged as **CORE** or **PERIPHERAL** (see `DISTILLATION_PROTOCOL.md` Section 5):
- **CORE** — Defines architecture, primary interfaces, main logic, Pydantic schemas. Read in full during Phase 1.
- **PERIPHERAL** — Secondary implementations, utilities, helpers, deprecated. Skimmed in Phase 1, read in full in Phase 2.

Format:
- `path/to/file.py` — [description] **(CORE)**
- `path/to/helper.py` — [description] **(PERIPHERAL)**

Volumes with ≤40 code files: all files are CORE (no tagging needed).

**Documentation to read**:
- [list of architecture docs, ADRs, guides, plans relevant to this subsystem]

**Test files to read** (for understanding expected behavior):
- [list of test files]

### A.3 Context Brief
What is already known from Volume 0 research about this subsystem. Includes:
- What worked in Attempt 3
- What failed or was never wired
- What was simulated/fake
- Relevant design principles from Volume 0 (by number: P1, P3, etc.)
- Relevant anti-patterns (A1, A3, etc.)
- Relevant rebuild requirements (R1, R2, etc.)

### A.4 Known Failures & Warnings
Specific failure modes observed in this subsystem during Attempt 3. These are traps the distillation agent must account for in the design spec.

---

## Part B: Design Specification (Agent Fills Out)

### B.1 Subsystem Purpose (Rebuild)
What this subsystem does in the rebuilt Atlas. Not what it did in Attempt 3 — what it SHOULD do. One paragraph max.

### B.2 Architecture Overview
High-level description of how the subsystem is structured. Include:
- Major components and their responsibilities
- Data flow (what comes in, what goes out)
- ASCII diagram if helpful

### B.3 Interface Contracts
For each public-facing component in this subsystem, define:
- **Input schema** (Pydantic model name and fields)
- **Output schema** (Pydantic model name and fields)
- **Methods/endpoints** exposed to other subsystems
- **Dependencies** consumed from other subsystems

Format:
```
Component: [name]
  Inputs: [schema name] — [field list with types]
  Outputs: [schema name] — [field list with types]
  Methods: [method signatures]
  Depends on: [other subsystem components]
  Depended on by: [who calls this]
```

### B.4 Scope Triage
For every component that existed in Attempt 3 (listed in source manifest), assign a verdict:

- **REBUILD** — Include in the new system. Specify what changes from Attempt 3.
- **DEFER** — Not in initial rebuild. Specify which phase it belongs to and why.
- **KILL** — Do not rebuild. Specify why (duplicated, unnecessary, wrong approach).

Every component must get a verdict. No omissions.

### B.5 Technology Choices
Specific libraries, frameworks, storage engines for this subsystem. Justify departures from defaults (Python 3.11+, FastAPI, Pydantic v2, SQLite, FAISS).

### B.6 Data Model
Pydantic schemas this subsystem owns. For each schema:
- Name
- Fields with types and constraints
- Validation rules
- Which memory layer(s) it persists to (if any)

### B.7 Error Handling
- Error types this subsystem defines (specific exception classes)
- How errors propagate (raise vs. log vs. return)
- Recovery strategies for each error type
- Reference Volume 0 P5: no silent failure

### B.8 Testing Strategy
Reference Volume 0 P11: Acceptance tests gate everything, not unit tests. Reference A8: tests that don't prove functionality.

**B.8.1 Acceptance tests (MANDATORY — define at least one)**
Each acceptance test must:
- Run against the live server (no mocks)
- Send real input through the full pipeline
- Verify real output matches expected behavior
- FAIL if this subsystem's implementation were deleted or stubbed

Describe the specific acceptance test(s): what input, what expected output, what endpoint or entry point, what constitutes a pass.

**B.8.2 Integration tests**
What cross-boundary interactions must be tested? These use real (test) databases and real subsystem instances — no mocks at boundaries.

**B.8.3 Unit tests**
What individual functions benefit from isolated testing? Mocks are allowed here. These are for development speed, not deployment gating.

**B.8.4 Attempt 3 regression tests**
Specific test cases that would have caught Attempt 3's failures in this subsystem. For each failure in A.4, define a test that prevents recurrence.

### B.9 Configuration
- What is configurable in this subsystem
- Default values
- How configuration is loaded (env vars, config file, etc.)
- Feature flags (if any) and their default state

### B.10 Subsystem Lessons Learned
What went wrong in THIS subsystem specifically during Attempt 3, beyond the system-wide lessons in Volume 0 Section 9. For each lesson:
- **What happened** — the specific failure or mistake
- **Why it happened** — root cause, not just symptoms
- **What the rebuild must do differently** — concrete design decision that prevents recurrence

These are not generic observations. "Code was too complex" is useless. "The memory manager grew to 1200 lines because every new layer added methods directly to it instead of using a plugin interface — the rebuild uses a registry pattern where each layer registers its own operations" is useful.

### B.11 Discoveries
Design decisions, patterns, or risks found during the deep dive that are NOT captured in Volume 0. These will be reviewed and potentially promoted to system-wide principles.

### B.12 Oversight Self-Review
**MANDATORY.** After completing all sections above, the distillation agent must re-read the entire volume and answer these questions:

1. **What would a programming agent still not know after reading this?** Identify gaps and fill them.
2. **What failure modes from Attempt 3 are not explicitly prevented by the design in B.2-B.9?** Add prevention mechanisms.
3. **Are there cross-volume dependencies that aren't documented?** (e.g., this subsystem depends on a schema defined in another volume). List them.
4. **Does the scope triage (B.4) have any omissions?** Every file in the source manifest must have a verdict.
5. **Are the interface contracts (B.3) specific enough to code against without ambiguity?**
6. **Does every design decision in this volume support Atlas-level performance?** Atlas is intended to be a Jarvis-level intelligence — proactive, autonomous, continuously learning, deeply personal. For each major design choice in B.2-B.6, ask: does this move Atlas toward that vision, or does it settle for "good enough"? If a decision limits future capability (e.g., a rigid schema that can't evolve, a synchronous pipeline that blocks real-time interaction, a single-user assumption that prevents multi-device presence), flag it and propose an alternative that preserves the path to full Jarvis-level performance.

Document findings and corrections made. If no oversights found, state what was checked and why it's complete.

### B.13 Design Quality Scorecard
**MANDATORY.** Before submission, score this volume's design on each criterion below (1-5). A score below 3 on any criterion means the design needs rework before programming agents touch it. The biggest waste of time is an engineer optimizing something that should not exist in the first place.

For each criterion, provide the score AND a one-sentence justification.

**Existence Justification (does this need to exist at all?)**
- **EJ-1: Right to exist** — Can Atlas reach Jarvis-level performance without this subsystem? If yes, why is it in the rebuild and not deferred? (1 = no justification, 5 = Atlas cannot reach Jarvis-level without this)
- **EJ-2: Scope discipline** — Is this the minimum viable version, or does it include speculative features? (1 = bloated with "might need later", 5 = every component has a concrete use case in the conversation loop)
- **EJ-3: Not reinventing** — Does this duplicate something available off-the-shelf? (1 = rebuilding what a library already does, 5 = genuinely novel or the off-the-shelf options don't fit)

**Design Fitness (is this the right design?)**
- **DF-1: Attempt 3 lessons applied** — Does this design explicitly prevent the failures documented in A.4 and B.10? (1 = same patterns repeated, 5 = every known failure has a structural prevention)
- **DF-2: Integration-first** — Could this subsystem be wired into the conversation loop TODAY, or does it need other unbuilt things? (1 = depends on 5 other unbuilt subsystems, 5 = works end-to-end with just memory + orchestrator)
- **DF-3: Evolvability** — Can this design grow toward Jarvis-level without a rewrite? (1 = locked into current assumptions, 5 = clear extension points for autonomy, multi-device, voice, learning)

**Buildability (can a programming agent actually build this?)**
- **BA-1: Specification completeness** — Could a programming agent build this subsystem using ONLY this volume + Volume 0, with zero questions? (1 = major ambiguities, 5 = every interface, schema, and behavior is specified)
- **BA-2: Testability** — Are the success criteria concrete enough to write tests against? (1 = vague "should work", 5 = specific inputs → expected outputs for every component)
- **BA-3: Size budget** — Is the estimated implementation size proportional to value? (1 = hundreds of files for marginal value, 5 = tight implementation for high value)

**Overall: [sum]/45** — Minimum passing score: 30/45. Below 30, the volume must be reworked.

---

**END OF TEMPLATE**

*The distillation agent's job is not done until B.12 is filled out. An incomplete B.12 means the volume is not ready for programming agents.*

---

## Modification History

| Version | Date | Modified By | Summary | Laymen Summary |
|---|---|---|---|---|
| v1 | 2026-03-10 | Oz | Initial creation — defined Part A/B structure, B.1-B.13 sections including acceptance tests (B.8), oversight self-review (B.12), design quality scorecard (B.13) | Created the fill-in-the-blank template that analysis agents use to document each subsystem |
| v2 | 2026-03-10 | Oz | Added documentation standard header/footer per PROJECT_CONVENTIONS.md Section 9 | Added tracking metadata so we know who changed what and when |
| v3 | 2026-03-10 | Oz | Added Doc ID field (`DB-X00-002`) per PROJECT_CONVENTIONS.md Section 9.4 | Added unique document number for machine searching |
| v4 | 2026-03-10 | Oz | Added CORE/PERIPHERAL tagging instructions to A.2 Source Manifest per DISTILLATION_PROTOCOL.md Section 5 | Added labels to source file lists so agents know which files to read in full vs. skim |
