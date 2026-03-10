# ATLAS Design Bible — Distillation Protocol

| Field | Value |
|---|---|
| **Doc ID** | `DB-X00-004` |
| **Name** | Distillation Protocol |
| **Purpose** | Defines the two-phase distillation process, integration gate, chunking rules, validation criteria, and agent instantiation method |
| **Owner** | Design Bible / Infrastructure |
| **Status** | `active` |
| **Supersedes** | N/A |
| **Superseded by** | N/A |
| **Author** | Oz |
| **Version** | v2 |
| **Created** | 2026-03-10 |
| **Last Modified** | 2026-03-10 |

---

## 1. Overview

Distillation is the process of extracting design intent from Atlas Attempt 3's codebase (516 Python files, 251,801 lines) into structured Design Bible volumes that programming agents can use to build Atlas v4 from scratch.

Each volume has a dedicated distillation agent. Agents do NOT coordinate directly with each other — they coordinate through their per-volume file in `design-bible/agent-comm/vol-XX.md` and the integration gate. The consolidated view in `AGENT_COMM.md` is read-only for agents.

**Two-phase approach prevents:**
- Agents making incompatible design decisions (caught at the gate)
- Agents producing volumes that duplicate or contradict each other (caught at gate review)
- Large context windows degrading quality (chunking protocol)

---

## 2. Phase 1: Shape Pass

**Goal:** Produce the high-level architecture and interface contracts for each subsystem. This is the skeleton — enough for the integration gate to detect conflicts and produce shared contracts.

**Scope:** Agents fill out **B.1 through B.4 only** (Purpose, Architecture Overview, Interface Contracts, Scope Triage).

**Process per agent:**
1. Read Volume 0 (`00-system-principles.md`) in full
2. Read their assigned volume's Part A (Identity, Source Manifest, Context Brief, Known Failures)
3. Read source files per the chunking protocol (Section 5)
4. Fill out B.1-B.4
5. Register any ownership claims, dependencies, or conflicts in `AGENT_COMM.md`
6. Submit Phase 1 output for integration gate review

**Time expectation:** One Warp session per volume. Phase 1 should be completable in a single session for all volumes.

**Output location:** The agent writes directly into their volume's Part B sections (B.1-B.4). The volume file itself is the output.

---

## 3. Integration Gate

**Trigger:** All 10 Phase 1 outputs are complete. The user verifies completeness before launching the gate agent.

**Gate agent reads:**
- Volume 0 (binding principles)
- All 10 volumes' B.1-B.4
- `AGENT_COMM.md` (all claims, dependencies, conflicts)
- `PROJECT_CONVENTIONS.md` (structural rules)

**Gate agent produces (in `design-bible/gate-output/`):**

### 3.1 conflict-report.md
Every detected cross-volume conflict. For each conflict:
- **What:** Description of the conflict
- **Volumes:** Which volumes disagree
- **Evidence:** Specific text from each volume that conflicts
- **Recommended resolution:** The gate agent's recommendation
- **Status:** `open` (user must resolve before Phase 2)

### 3.2 shared-contracts.md
Interface contracts that span volumes. These become binding constraints for Phase 2.
- Shared Pydantic schemas (types that cross subsystem boundaries)
- API boundary contracts (who calls what)
- Memory layer interface (how subsystems interact with memory)
- Event/message contracts (if any subsystem uses events)

### 3.3 build-order-refined.md
Refined build order based on actual dependency analysis from Phase 1 outputs. This may differ from Volume 0's initial build order (Section 13). The refined version takes precedence once approved.

### 3.4 mva-refined.md
Refined MVA (Minimum Viable Atlas) criteria. May add, remove, or modify acceptance tests based on what Phase 1 revealed about the actual system shape.

### 3.5 quality-flags.md
Per-volume quality assessment:
- **PASS:** Volume is ready for Phase 2
- **REWORK:** Volume has gaps or inconsistencies — specific items listed
- **INCOMPLETE:** Agent missed required sections or files

**Gate acceptance criteria (ALL must be true):**
1. Every conflict in `conflict-report.md` has a resolution (user-approved)
2. `shared-contracts.md` covers every cross-volume interface identified in `AGENT_COMM.md`
3. Build order is a valid DAG with no cycles
4. No volume has `INCOMPLETE` status
5. User explicitly approves the gate output

**After gate approval:** User commits gate output to git. Phase 2 begins.

---

## 4. Phase 2: Deep Dive

**Goal:** Complete the full design specification for each subsystem, constrained by the approved shared contracts.

**Scope:** Agents fill out **B.5 through B.13** (Technology, Data Model, Errors, Testing, Config, Lessons, Discoveries, Self-Review, Scorecard).

**Process per agent:**
1. Re-read their volume's Part A and Phase 1 output (B.1-B.4)
2. Read `design-bible/gate-output/shared-contracts.md` — these are now binding constraints
3. Read any conflict resolutions relevant to their volume
4. Read ALL source files (full content, multiple passes if needed — no more skimming)
5. Fill out B.5-B.13
6. Complete B.12 (Oversight Self-Review) — MANDATORY
7. Complete B.13 (Design Quality Scorecard) — minimum passing score: 30/45
8. Update `design-bible/agent-comm/vol-XX.md` (your per-volume file) with any new claims or dependencies discovered. Do **NOT** edit `AGENT_COMM.md` directly — it is read-only for agents.
9. Submit completed volume

**Constraint enforcement:** If a Phase 2 agent's design contradicts an approved shared contract, the contract wins. The agent must either conform or flag a contract revision request in their per-volume agent-comm file.

---

## 5. Chunking Protocol (Large Volumes)

**Threshold:** If a volume's source manifest exceeds ~40 code files, the agent must use the chunking protocol instead of attempting to read everything at once.

**Volume file counts:**

| Volume | Code Files | Chunking Required |
|---|---|---|
| Vol 01 (Memory) | 43 | Yes |
| Vol 02 (Orchestrator) | 77 | Yes |
| Vol 03 (Learning) | 70 | Yes |
| Vol 04 (Self-modification) | 58 | Yes |
| Vol 05 (Intelligence) | 11 | No (all CORE) |
| Vol 06 (Voice) | 11 | No (all CORE) |
| Vol 07 (Console) | 91 | Yes |
| Vol 08 (API) | 40 | Yes (borderline) |
| Vol 09 (Governance) | 12 | No (all CORE) |
| Vol 10 (External Tools) | 42 | Yes |

**Chunking process (Phase 1):**
1. Read all **CORE** files in full (these are tagged in the volume's A.2 Source Manifest)
2. For **PERIPHERAL** files, read only: module docstring, class definitions, function signatures, import statements, and Pydantic schemas. Skip implementation bodies.
3. Produce B.1-B.4 from this partial read

**Chunking process (Phase 2):**
1. Read ALL files in full (CORE and PERIPHERAL). If context is too large for a single pass:
   - Pass 1: CORE files + all schemas/interfaces → draft B.5-B.10
   - Pass 2: PERIPHERAL files → refine B.5-B.10 and complete B.11-B.13
2. Every file in the source manifest must be read in full by the end of Phase 2

**CORE/PERIPHERAL classification criteria:**
- **CORE:** Files that define the subsystem's architecture, primary interfaces, main logic, and Pydantic schemas. These are the files a programming agent would need to understand the design intent.
- **PERIPHERAL:** Files that are secondary implementations, utilities, helpers, deprecated versions, or specialized extensions. Important for completeness but not for architectural understanding.

Each volume's A.2 section tags every file. See individual volumes for specific tags.

---

## 6. External Validation Rules

Quality is enforced at two levels: self-review (B.12) and external validation (integration gate + user).

### 6.1 B.13 Score Validation
The integration gate agent independently scores each volume's design quality using the B.13 scorecard criteria. If the gate agent's score differs from the distillation agent's self-score by more than 5 points (out of 45), the volume is flagged for rework.

### 6.2 B.12 Completeness Check
The integration gate validates B.12 by checking: does the self-review mention every item from A.4 (Known Failures & Warnings)? If any A.4 item is not addressed in B.12, the volume is marked `INCOMPLETE`.

### 6.3 Scope Triage Completeness
B.4 must assign a verdict (REBUILD/DEFER/KILL) to every code file listed in A.2. The gate agent verifies file count matches.

### 6.4 Interface Contract Consistency
For each DEPENDENCY declared in `AGENT_COMM.md` (or the per-volume agent-comm files), both the provider and consumer volumes must have matching interface definitions in B.3. Mismatches are flagged as conflicts.

---

## 7. Final Review

After all 10 Phase 2 volumes are submitted, the integration gate agent performs a final review:

1. Re-read all 10 completed volumes
2. Verify all shared contracts are satisfied
3. Verify all conflicts are resolved
4. Produce a final quality report
5. Identify any remaining gaps that coding agents would encounter

The final review output goes to `design-bible/gate-output/final-review.md`.

**Definition of done:** All volumes score ≥30/45, all contracts satisfied, all conflicts resolved, user approves.

---

## 8. Agent Instantiation

### 8.1 Method
Each distillation agent is a Warp agent session. The user launches the session with a system prompt derived from the templates in `design-bible/prompts/`.

### 8.2 Prompt Templates

**Location:** `design-bible/prompts/`

| Template | Used For | Placeholders |
|---|---|---|
| `distill-phase1.md` | Phase 1 distillation agents | `{{VOLUME_NUMBER}}`, `{{VOLUME_NAME}}`, `{{SOURCE_MANIFEST_PATH}}` |
| `distill-phase2.md` | Phase 2 distillation agents | `{{VOLUME_NUMBER}}`, `{{VOLUME_NAME}}`, `{{VOLUME_NUMBER_PADDED}}`, `{{SOURCE_MANIFEST_PATH}}`, `{{CONTRACTS_PATH}}` |
| `integration-gate.md` | Integration gate agent | `{{PHASE}}` (1 or final) |
| `coding-agent.md` | Coding agents (post-distillation) | `{{SUBSYSTEM}}`, `{{VOLUME_PATH}}`, `{{TIER}}` |

### 8.3 Launch Sequence

**For distillation (Phase 1):**
1. User opens the prompt template `design-bible/prompts/distill-phase1.md`
2. User fills in the placeholders for the target volume
3. User creates a new Warp agent session with the filled prompt as system context
4. Agent reads assigned files and produces B.1-B.4 output
5. User reviews output, requests revisions if needed
6. User commits the volume update to git
7. Repeat for each volume (can run in parallel for independent volumes)

**For integration gate:**
1. User ensures all 10 Phase 1 outputs are committed
2. User opens `design-bible/prompts/integration-gate.md`, fills in `{{PHASE}}` = 1
3. User creates Warp agent session with the filled prompt
4. Gate agent reads all volumes and produces gate output
5. User reviews and resolves conflicts
6. User approves and commits gate output

**For distillation (Phase 2):**
Same as Phase 1, but using `distill-phase2.md` template. The agent also reads the approved gate output.

**Parallelism rules:**
- Phase 1: All 10 volumes can run in parallel (no cross-dependencies at this stage)
- Integration gate: Sequential (one gate agent)
- Phase 2: Volumes can run in parallel, but volumes with unresolved dependencies (per `AGENT_COMM.md` / `agent-comm/`) should be sequenced so the provider completes first

---

## 9. Rules Summary

1. **Volume 0 is binding.** Every design decision must align with the principles, anti-patterns, and requirements in Volume 0.
2. **Agent-comm files are the coordination hub.** Each agent writes to `design-bible/agent-comm/vol-XX.md`. The consolidated `AGENT_COMM.md` is read-only for agents; the integration gate merges per-volume files into it after each phase.
3. **Shared contracts are binding after gate approval.** Phase 2 agents must conform.
4. **No skipping sections.** Every Part B section must be filled. N/A is acceptable with a reason.
5. **B.12 and B.13 are mandatory.** Incomplete volumes are rejected.
6. **CORE/PERIPHERAL tags must be respected.** In Phase 1, PERIPHERAL files are skimmed. In Phase 2, all files are read in full.
7. **The user has final approval at every gate.** No phase transition happens without explicit user approval.

---

## Modification History

| Version | Date | Modified By | Summary | Laymen Summary |
|---|---|---|---|---|
| v1 | 2026-03-10 | Oz | Initial creation — defined two-phase distillation, integration gate protocol (5 output documents), chunking protocol for large volumes, external validation rules, agent instantiation via Warp session prompts | Created the master playbook for how analysis agents extract design knowledge from the old codebase |
| v2 | 2026-03-10 | Oz | Updated §1, §4, §6.4, §8.2, §8.3, §9 to reference per-volume agent-comm files (`agent-comm/vol-XX.md`) instead of directing agents to write to `AGENT_COMM.md`. Added `{{VOLUME_NUMBER_PADDED}}` to §8.2 template table. | Updated coordination rules so agents write to their own file instead of all fighting over one shared file |
