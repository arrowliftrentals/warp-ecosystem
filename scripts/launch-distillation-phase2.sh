#!/usr/bin/env bash
# Launch Phase 2 distillation — 10 cloud agents in parallel
# Each agent fills B.5-B.13 for its assigned volume.

set -o pipefail

ENV_ID="CidMkD7duAR9h9e2HB8gzG"
BRANCH="design-bible"
CONTRACTS="design-bible/gate-output/shared-contracts.md"

VOLUMES=(
    "1:Memory System:design-bible/01-memory-system.md:01"
    "2:Orchestrator:design-bible/02-orchestrator.md:02"
    "3:Learning:design-bible/03-learning.md:03"
    "4:Self-Modification:design-bible/04-self-modification.md:04"
    "5:Intelligence:design-bible/05-intelligence.md:05"
    "6:Voice & Multimodal:design-bible/06-voice-multimodal.md:06"
    "7:Console:design-bible/07-console.md:07"
    "8:API & Infrastructure:design-bible/08-api-infrastructure.md:08"
    "9:Governance:design-bible/09-governance.md:09"
    "10:External Tools:design-bible/10-external-tools.md:10"
)

PROMPT_TEMPLATE='# Phase 2 Distillation Agent — Volume {{NUM}}: {{NAME}}

## Your Role
You are a distillation agent completing the full design specification for **Volume {{NUM}}: {{NAME}}**.

This is **Phase 2 (Deep Dive)**. B.1-B.4 are already filled from Phase 1. You complete B.5-B.13.

## Reading Order (STRICT)
1. Read `design-bible/00-system-principles.md` (Volume 0) — binding
2. Read `design-bible/DISTILLATION_PROTOCOL.md` — your operating rules
3. Read `design-bible/PROJECT_CONVENTIONS.md` — structural rules
4. Read `{{MANIFEST}}` — your volume (Part A + Phase 1 output in B.1-B.4)
5. Read `{{CONTRACTS}}` (`design-bible/gate-output/shared-contracts.md`) — **BINDING.** Your design must conform to these contracts.
6. Read `design-bible/gate-output/conflict-report.md` — check for resolutions affecting your volume
7. Read `design-bible/gate-output/quality-flags.md` — check for rework items flagged against your volume
8. Read `design-bible/agent-comm/vol-{{PAD}}.md` — your volume existing claims, dependencies, and conflict acknowledgements
9. Read ALL source files in A.2 in full (CORE and PERIPHERAL). Use multi-pass if needed:
   - Pass 1: CORE files + all schemas/interfaces → draft B.5-B.10
   - Pass 2: PERIPHERAL files → refine B.5-B.10, complete B.11-B.13

## Output Requirements
Fill out B.5 through B.13:

- **B.5 Technology Choices** — Libraries, frameworks, storage. Justify departures from defaults.
- **B.6 Data Model** — Pydantic schemas this subsystem owns. Fields, types, constraints, validation rules.
- **B.7 Error Handling** — Error types, propagation, recovery. Reference Volume 0 P5.
- **B.8 Testing Strategy** — Acceptance tests (mandatory), integration tests, unit tests, regression tests from A.4 failures.
- **B.9 Configuration** — What configurable, defaults, how loaded, feature flags.
- **B.10 Subsystem Lessons Learned** — What went wrong specifically in this subsystem. Concrete, not generic.
- **B.11 Discoveries** — Patterns or risks not in Volume 0. May be promoted to system-wide principles.
- **B.12 Oversight Self-Review** — MANDATORY. Answer all 6 questions. Document findings and corrections made.
- **B.13 Design Quality Scorecard** — MANDATORY. Score all 9 criteria (1-5). Minimum passing: 30/45.

## Constraints
- Shared contracts from `{{CONTRACTS}}` are binding.
- Every file in the source manifest must be read in full by the end of Phase 2.
- B.12 must mention every item from A.4 (Known Failures & Warnings). Missing items = INCOMPLETE.
- B.4 verdicts from Phase 1 cannot be changed without documenting the reason in B.11.

## Rules
- Volume 0 principles override your judgment.
- Be specific. A programming agent builds from this volume + Volume 0 alone, with zero questions.
- Do not copy code. Describe design intent, interfaces, and behavior.
- Update `design-bible/agent-comm/vol-{{PAD}}.md` with any new claims or dependencies discovered during deep dive. Do **NOT** edit `AGENT_COMM.md` directly — it is read-only for distillation agents.
- If shared contracts from `{{CONTRACTS}}` conflict with your design, flag it in your per-volume agent-comm file, not in `AGENT_COMM.md`.

## Git Workflow
1. Create branch: `git checkout -b distill/vol-{{PAD}}`
3. Make your changes to `{{MANIFEST}}` and `design-bible/agent-comm/vol-{{PAD}}.md`
4. Commit with: `git add -A && git commit -m "docs(vol-{{NUM}}): Phase 2 distillation — B.5-B.13"`
5. Push: `git push origin distill/vol-{{PAD}}`'

echo "=== Launching Phase 2 Distillation (10 agents) ==="
echo ""

for entry in "${VOLUMES[@]}"; do
    IFS=':' read -r num name manifest pad <<< "$entry"

    prompt="${PROMPT_TEMPLATE}"
    prompt="${prompt//\{\{NUM\}\}/$num}"
    prompt="${prompt//\{\{NAME\}\}/$name}"
    prompt="${prompt//\{\{MANIFEST\}\}/$manifest}"
    prompt="${prompt//\{\{PAD\}\}/$pad}"
    prompt="${prompt//\{\{CONTRACTS\}\}/$CONTRACTS}"

    echo "Launching: Vol $num ($name) → distill/vol-$pad"
    oz agent run \
        -e "$ENV_ID" \
        -n "Phase2-Vol$num-$name" \
        --prompt "$prompt" &

    sleep 2
done

echo ""
echo "All 10 agents launched. Monitor with: oz agent list"
wait
