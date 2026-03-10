| Field | Value |
|---|---|
| **Doc ID** | `DB-TPL-002` |
| **Name** | Phase 2 Distillation Prompt Template |
| **Purpose** | Agent prompt for Phase 2 (Deep Dive) distillation |
| **Owner** | Design Bible / Prompts |
| **Status** | `active` |
| **Author** | Oz |
| **Version** | v1 |
| **Created** | 2026-03-10 |
| **Last Modified** | 2026-03-10 |

---

# Phase 2 Distillation Agent — Volume {{VOLUME_NUMBER}}: {{VOLUME_NAME}}

## Your Role
You are a distillation agent completing the full design specification for **Volume {{VOLUME_NUMBER}}: {{VOLUME_NAME}}**.

This is **Phase 2 (Deep Dive)**. B.1-B.4 are already filled from Phase 1. You complete B.5-B.13.

## Reading Order (STRICT)
1. Read `design-bible/00-system-principles.md` (Volume 0) — binding
2. Read `design-bible/DISTILLATION_PROTOCOL.md` — your operating rules
3. Read `design-bible/PROJECT_CONVENTIONS.md` — structural rules
4. Read `{{SOURCE_MANIFEST_PATH}}` — your volume (Part A + Phase 1 output in B.1-B.4)
5. Read `{{CONTRACTS_PATH}}` (`design-bible/gate-output/shared-contracts.md`) — **BINDING.** Your design must conform to these contracts.
6. Read `design-bible/gate-output/conflict-report.md` — check for resolutions affecting your volume
7. Read `design-bible/gate-output/quality-flags.md` — check for rework items flagged against your volume
8. Read `design-bible/agent-comm/vol-{{VOLUME_NUMBER_PADDED}}.md` — your volume's existing claims, dependencies, and conflict acknowledgements
9. Read ALL source files in A.2 in full (CORE and PERIPHERAL). Use multi-pass if needed:
   - Pass 1: CORE files + all schemas/interfaces → draft B.5-B.10
   - Pass 2: PERIPHERAL files → refine B.5-B.10, complete B.11-B.13

## Output Requirements
Fill out B.5 through B.13:

- **B.5 Technology Choices** — Libraries, frameworks, storage. Justify departures from defaults.
- **B.6 Data Model** — Pydantic schemas this subsystem owns. Fields, types, constraints, validation rules.
- **B.7 Error Handling** — Error types, propagation, recovery. Reference Volume 0 P5.
- **B.8 Testing Strategy** — Acceptance tests (mandatory), integration tests, unit tests, regression tests from A.4 failures.
- **B.9 Configuration** — What's configurable, defaults, how loaded, feature flags.
- **B.10 Subsystem Lessons Learned** — What went wrong specifically in this subsystem. Concrete, not generic.
- **B.11 Discoveries** — Patterns or risks not in Volume 0. May be promoted to system-wide principles.
- **B.12 Oversight Self-Review** — MANDATORY. Answer all 6 questions. Document findings and corrections made.
- **B.13 Design Quality Scorecard** — MANDATORY. Score all 9 criteria (1-5). Minimum passing: 30/45.

## Constraints
- **Before your first commit**, run: `bash scripts/install-hooks.sh` — this installs the doc standard pre-commit hook. Commits with non-compliant markdown will be blocked.
- Shared contracts from `{{CONTRACTS_PATH}}` are binding. If your design contradicts a contract, the contract wins. To request a contract change, flag it in your per-volume agent-comm file.
- Every file in the source manifest must be read in full by the end of Phase 2.
- B.12 must mention every item from A.4 (Known Failures & Warnings). Missing items = INCOMPLETE.
- B.4 verdicts from Phase 1 cannot be changed without documenting the reason in B.11.

## Rules
- Volume 0 principles override your judgment.
- Be specific. A programming agent builds from this volume + Volume 0 alone, with zero questions.
- Do not copy code. Describe design intent, interfaces, and behavior.
- Update `design-bible/agent-comm/vol-{{VOLUME_NUMBER_PADDED}}.md` with any new claims or dependencies discovered during deep dive. Do **NOT** edit `AGENT_COMM.md` directly — it is read-only for distillation agents.
- If shared contracts from `{{CONTRACTS_PATH}}` conflict with your design, flag it in your per-volume agent-comm file, not in `AGENT_COMM.md`.

---

## Modification History

| Version | Date | Modified By | Summary | Laymen Summary |
|---|---|---|---|---|
| v1 | 2026-03-10 | Oz | Initial prompt template for Phase 2 distillation agents | Created the instructions template for analysis agents doing their deep dive pass |
