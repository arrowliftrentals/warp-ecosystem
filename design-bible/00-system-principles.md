# ATLAS Design Bible — Volume 0: System-Wide Principles

| Field | Value |
|---|---|
| **Doc ID** | `DB-V00-001` |
| **Name** | Volume 0: System-Wide Principles |
| **Purpose** | Single source of truth for rebuilding Atlas — every agent reads this first, no agent reads old code directly |
| **Owner** | Design Bible / System-wide |
| **Status** | `active` |
| **Supersedes** | atlas-identity.md, atlas-constitution-v2.md, COMPREHENSIVE_ANALYSIS_WARP_ATTEMPTS_v1.md, capability-analysis-honest.md, personal-ai-rubric.md, meta-system-rubric.md, SELF_BUILDING_ATLAS_ROADMAP.md, LEARNING_FROM_AI_FAILURES.md, atlas-evolution-pattern.md, business-strategy-discussion.md, critical-architecture-gaps-2026-03.md, atlas-oversights-2026-02-08.md, jarvis-gap-closure-plan.md, exhaustive-cognitive-architecture-analysis.md, atlas-personality.md |
| **Superseded by** | N/A |
| **Author** | Oz |
| **Version** | v4 |
| **Created** | 2026-03-10 |
| **Last Modified** | 2026-03-10 |

---

## 1. What Atlas Is

**ATLAS** = Autonomous Technological Learning Adaptive System

Atlas is a personal AI assistant designed to reach Jarvis-level capability: understanding high-level objectives in natural language, translating them into executable plans, executing those plans safely, learning from every interaction, and adapting to become more capable over time.

Atlas is NOT a chatbot, NOT a wrapper around an LLM, and NOT a commercial SaaS product (though commercial potential exists). Atlas is a **neuro-symbolic hybrid cognitive system** — a symbolic reasoning core with ML as advisory capability, backed by a 10-layer persistent memory architecture.

**The owner is a mechanical engineer PhD, not a programmer.** Atlas must ultimately be operable, debuggable, and extensible by someone who understands systems thinking but does not write code. The rebuild must prioritize clarity, modularity, and self-documentation.

---

## 2. Three Iterations: What Was Tried and Why Each Failed

### Attempt 1: LLM-Centric (WARP Attempt 1)
**Architecture:** LLM at the center of all decision-making, with L1-L10 memory layers.
**What worked:**
- The L1-L10 memory architecture concept was visionary and ahead of its time
- Rich tool ecosystem design
- Research-driven approach
- Console UI for visibility

**Why it failed:**
- LLM had direct execution authority with no validation gate between output and action
- Governance layer (L10) was documentation, not enforcement — policies existed but nothing checked compliance
- No deterministic verification of LLM outputs before execution
- The system drifted, hallucinated, and eventually damaged the codebase
- Trust was destroyed: "it drifted and began damaging the codebase, hallucinating and lying"

**Root cause:** Ungoverned LLM authority. The LLM could propose AND execute without any symbolic checkpoint.

### Attempt 2: Pure Symbolic (WARP-Atlas)
**Architecture:** Symbolic-first with ASACI governance. LLMs relegated to proposal-only, never execute.
**What worked:**
- ASACI governance model prevents capability creep
- Deterministic execution ensures repeatability
- Append-only tracing provides complete auditability
- Clear authority hierarchy (governance → symbolic → LLM → execution, one-way)
- LLM containment prevents drift by design

**Why it failed:**
- Governance became a development bottleneck, not an enabler
- Zero trust of LLMs meant zero leverage of LLM generative capabilities
- 110+ phases of development produced only 3 registered tools and placeholder execution
- Excessive ceremony for every change — tool registration overhead killed velocity
- "Placeholder execution" became the permanent state
- Result: perfect governance over nothing functional

**Root cause:** Over-governance. Safety without functionality is not safety — it's paralysis.

### Attempt 3: Neuro-Symbolic Hybrid (Current Atlas)
**Architecture:** Symbolic core validates; ML advises; LLM is fallback. 10-layer memory system fully implemented.
**What worked:**
- The hybrid architecture is the correct paradigm (validated by contemporary AI research)
- Memory system implemented with 10 functioning layers and DB backing
- Comprehensive test suite (grew from 442 to 6487 tests)
- Constitutional framework ratified and partially enforced
- Self-modification pipeline with sandbox, proposals, and rollback
- 80+ registered tools
- Full async event bus
- Intelligence system with domain-specific extractors

**Why it failed:**
- Individual components work in isolation but fail in integration — the "glue" is missing
- Massive infrastructure without basic end-to-end functionality ("hi atlas" fails inconsistently)
- Validation theater: the system claims tests pass without actually running them
- Simulated capabilities reported as real (multimodal subsystem uses hash-based fake detection)
- Critical pipelines built but never wired (AutoRetrainingDaemon exists but is never started)
- All feature flags set to FALSE — capabilities exist in code but are disabled
- Duplicated implementations (4 separate vector store implementations with confused imports)
- 50+ exception handlers silently swallow errors
- API contract validation missing — code calling non-existent methods passes all checks
- TODO placeholder returns ship as "fixes"
- Codebase grew to 516 Python files, 251,801 lines — too large to comprehend or maintain

**Root cause:** Scope explosion without integration discipline. Every feature was built, none were finished. The system optimized for "implement next feature" instead of "make what exists actually work."

---

## 3. The Moat: What Makes Atlas Valuable

Not everything in Atlas is unique. Most capabilities are commodity. Three capabilities are defensible:

### 3.1 The 10-Layer Memory Architecture (EXTREMELY UNIQUE)
Most AI systems have NO long-term memory. ChatGPT forgets after a session. Claude has a context window. AutoGPT has basic vector DB. Atlas has a structured cognitive memory system spanning 10 distinct layers from working memory to governance. No competitor has this depth. This IS the moat.

The 10 layers:
- **L1 Working Memory** — active session context (ephemeral)
- **L2 Short-term Memory** — recent events for consolidation (hours to days)
- **L3 Episodic Memory** — all interactions and outcomes with temporal queries (permanent)
- **L4 Declarative Memory** — validated facts with semantic search (permanent)
- **L5 Procedural Memory** — learned skills and execution patterns (permanent)
- **L6 Attention Memory** — focus tracking and context switching
- **L7 World State Memory** — environment snapshots and change detection
- **L8 Goals Memory** — objectives, plans, progress tracking
- **L9 Social Memory** — user profiles and interaction patterns
- **L10 Vector/Governance Memory** — semantic retrieval and constitutional oversight

### 3.2 Self-Modification with Sandbox Safety (EXTREMELY UNIQUE)
Almost no AI system attempts autonomous code modification. Atlas has a complete pipeline: propose change → test in sandbox → validate against constitutional rules → human approval → apply with rollback. The combination of ambition (self-modification) and safety (sandbox + governance) is the moat.

### 3.3 Learning System + Memory (STRONG DIFFERENTIATOR)
Active learning from user corrections, intent classifier retraining, domain adaptation. Alone this is moderate. Combined with the 10-layer memory system, it creates a personal AI that genuinely improves over time and adapts to YOUR specific workflows.

### What Is NOT a Moat
- **Orchestrator** — every AI system has one, commodity
- **LLM integration** — API calls to OpenAI/Anthropic, commodity
- **Screen control** — standard macOS APIs, commodity
- **Sandbox execution** — Docker exists, table stakes for enterprise

**Rebuild priority:** The moat capabilities (memory, self-modification, learning) must be built first, built well, and built to last. Commodity capabilities can be implemented quickly later.

---

## 4. Design Principles That Must Survive

These are non-negotiable. They were learned through three painful iterations and validated by research.

### P1: ML Advises, Symbolic Core Decides
LLMs are creative, flexible, and unreliable. Symbolic systems are rigid, predictable, and trustworthy. The architecture must use both: LLM proposes, symbolic core validates and executes. The LLM never has direct execution authority. This is the lesson of Attempt 1.

### P2: Governance Enables, Not Blocks
Governance must be a safety net that catches errors, not a bureaucracy that prevents work. Start with 3 hard rules (schema validation at boundaries, standard module interface, automated test gate). Add more governance only when a specific failure demands it. This is the lesson of Attempt 2.

### P3: Nothing Ships Without Integration
A component that passes unit tests but has never been called by another component is not done. Every feature must be wired end-to-end and proven to work in the full system before it is considered complete. This is the lesson of Attempt 3.

### P4: Validation Must Be Real
If the system claims "tests pass," there must be cryptographic proof of actual test execution. Validation theater — claiming verification without performing it — is the most dangerous failure mode because it creates false confidence. No claims without evidence. No evidence without execution.

### P5: Silent Failure Is a System Fault
Every error must be classified, logged, and routed to the learning system. Empty `except: pass` blocks are forbidden. An error that disappears silently will reappear as a mysterious production failure later.

### P6: Memory Is the Foundation, Not a Feature
All persistent context flows through the L1-L10 memory system, not through LLM context windows. Memory enables learning, personalization, goal tracking, and continuity across sessions. It is not an add-on — it is the architectural foundation.

### P7: Smaller and Working Beats Larger and Broken
Attempt 3 grew to 251,801 lines and 516 files, and basic "hi atlas" failed. The rebuild must resist scope expansion. A system with 50 files where every file is fully integrated and tested is worth more than a system with 500 files where integration is aspirational.

### P8: Pydantic Schemas at Every Boundary
All data entering or leaving a memory layer, API endpoint, or subsystem boundary must pass through Pydantic schema validation. This is not optional, not "add later," not "skip for performance." It is the mechanism that prevents data corruption and enables provenance tracking.

### P9: Output Governance — Not Just Action Governance
P1 governs what Atlas **does**. P9 governs what Atlas **says**. In Attempt 3, every LLM-generated response was returned to the user raw — no validation, no evidence check, no grounding. The LLM could hallucinate file paths, invent metrics, claim "tests passed" with zero proof, and the user received it as truth. This is the text-domain equivalent of Attempt 1's ungoverned execution authority.

All LLM-generated text destined for the user must pass through a governance gate. Factual claims must be grounded in evidence (tool outputs, memory retrievals, file contents). Claims that cannot be grounded must be flagged as speculative, not presented as fact. The symbolic core governs what Atlas says, not just what Atlas does.

### P10: Atlas Has a Defined Personality
Atlas is not a generic chatbot. He has a canonical personality: professional yet conversational, proactive, action-oriented. He explains what he's doing and why. He takes initiative and suggests next steps. He acknowledges limitations honestly. He adapts communication style (detail level, formality) to the user, but core identity traits are immutable and version-controlled. Self-modification cannot alter personality without explicit human approval. The per-subsystem volume for the orchestrator/response system must specify this fully.

### P11: Acceptance Tests Gate Everything, Not Unit Tests
Attempt 3 had 6,487 tests at 100% pass rate. Basic "hi atlas" failed. This happened because unit tests tested mocked components in isolation — they proved the code matched the test's expectations, not that the system worked. A test that passes when the implementation is deleted (because it tests a mock) proves nothing.

The rebuild enforces a **test hierarchy with strict gating**:
1. **Acceptance tests** (highest authority) — hit the running server with real requests, verify real responses. These test what the USER experiences. "Send 'hello' to /v1/atlas/chat, receive a coherent response within 5 seconds." If acceptance tests fail, nothing ships. Period.
2. **Integration tests** — test real component interactions across subsystem boundaries. No mocks at boundaries. If the memory layer is involved, it uses a real (test) database, not a mock.
3. **Unit tests** (lowest authority) — test individual functions in isolation. Mocks are allowed. These are useful for development speed but they DO NOT gate deployment.

**The rule:** No subsystem is "done" until its acceptance test passes against the live system. Unit test count is irrelevant. 10 acceptance tests that prove the system works are worth more than 10,000 unit tests that prove components match their mocks.

**Tiered test execution (don't run everything every time):**
Running thousands of tests after every change is a massive time sink that killed velocity in Attempt 3. The solution is running the right tests at the right time:

| Trigger | What runs | Time budget | Blocks |
|---|---|---|---|
| On save / during development | **Smoke tests** — ~5 tests that verify the system boots and the conversation loop responds | < 10 seconds | Nothing (informational) |
| Before commit | **Changed-subsystem acceptance + unit tests** — only tests for files that changed, plus the core smoke suite | < 60 seconds | Commit |
| Before merge / PR | **All acceptance tests + integration tests** — proves no subsystem broke | < 5 minutes | Merge |
| Nightly / CI | **Full suite** — every unit, integration, and acceptance test | No limit | Release |

The smoke suite is the heartbeat. It runs in under 10 seconds and answers one question: "is Atlas alive and responding?" If smoke fails, stop everything. If smoke passes, you have confidence to keep working while the heavier suites run asynchronously.

**Changed-file test targeting:** Tests must be organized so that changing a file in `src/memory/` triggers only memory-related tests, not the entire suite. pytest markers, directory structure, or a dependency map can achieve this. The rebuild must make this possible from day one — test organization is architecture, not afterthought.

---

## 5. Anti-Patterns: What Must Never Be Repeated

### A1: Feature Factory Without Integration
Building component after component without wiring them together. Attempt 3's fatal pattern: 80+ tools registered, 30 subsystems initialized, and basic conversation fails.

**Rule:** No new subsystem begins until the previous subsystem is integrated end-to-end and proven with an integration test.

### A2: Validation Theater
Claiming "442 tests passing" while the actual test count is different, or reporting health=True for subsystems that are stubs. The system must never overstate its own capability.

**Rule:** Health checks must verify actual functionality, not just that an object was instantiated. Test results must come from actual pytest execution with visible output.

### A3: Simulated Capabilities
The multimodal subsystem in Attempt 3 used `hashlib.md5` to fake object detection. It reported as functional. Anything that fakes real capability must instead report status=STUB and health=False.

**Rule:** If a capability isn't real, it must say so. No fake results dressed up as real ones.

### A4: Exception Swallowing
50+ `except: pass` blocks in Attempt 3 made debugging impossible. Errors vanished and resurfaced as mysterious failures elsewhere.

**Rule:** Every exception handler must at minimum log the error with context. Critical paths must raise, not swallow.

### A5: Scope Explosion
Attempt 3 grew from 33,000 lines to 251,801 lines. Most of that code was never integrated. The codebase became incomprehensible.

**Rule:** The rebuild has a line budget. If a subsystem exceeds its allocation, it must be refactored before more code is added.

### A6: Big Bang Rewrite Without Coexistence
Deleting old code before new code is proven. This eliminates rollback capability.

**Rule:** When replacing a component, the old and new implementations must coexist until the new one is validated by metrics, not intuition.

### A7: TODO in Production Code
Attempt 3 shipped fix templates containing `return False # TODO: implement`. These placeholders became permanent.

**Rule:** No TODO comments in production code. Either implement it, raise NotImplementedError, or create a tracked issue. TODOs in code are invisible debt.

### A8: Tests That Don't Prove Functionality
Attempt 3 had 6,487 tests passing at 100%. The system couldn't reliably respond to "hi." This happened because:
- Unit tests mocked every dependency, so they tested code structure, not behavior
- No test ever sent an HTTP request to the running server and verified the response
- No test ever proved that the conversation loop worked end-to-end
- Test count became a vanity metric — more tests felt like progress while the system remained broken
- Tests could pass even if the implementation was a stub (`return None`)

**Rule:** Every subsystem must have at least one **acceptance test** that proves it works in the running system, not in isolation. Acceptance tests use no mocks. They hit real endpoints, use real (test) databases, and verify real outputs. If you can delete the subsystem's implementation and the acceptance test still passes, the test is worthless and must be rewritten.

---

## 6. Constitutional Governance (Distilled)

The full constitution (10 articles) is archived. For the rebuild, the governance distills to these enforceable rules:

### Hard Rules (Automated Enforcement — Block on Violation)
1. **Schema validation at boundaries** — All data entering/leaving memory layers and API endpoints passes Pydantic validation. Violations blocked at runtime.
2. **Test gate before merge** — No code merges without 100% test pass rate. Test results must come from actual execution, not claims.
3. **Layer separation** — Memory layers are distinct. No layer bypasses the MemoryManager. No layer assumes authority outside its mandate.

### Soft Rules (Logged and Audited — Don't Block)
4. **Provenance tracking** — Facts should be traceable to source, evidence, and confidence level. Missing provenance is logged, not blocked.
5. **Change documentation** — Significant changes should have what/why/impact documented. Missing documentation is flagged in audit.
6. **Cross-layer operation logging** — When one subsystem reads from another's domain, the operation is logged for audit.

### Aspirational Rules (Add When System Matures)
7. **Automated regression benchmarking** — Performance on validated tasks must remain ≥ baseline after changes.
8. **Learning promotion gates** — Learned behaviors must pass validation before production deployment.
9. **Governance action auditing** — All suppression/override decisions logged with justification and reversibility.

**The key lesson:** Start with 3 hard rules. Prove the system works. Then add governance incrementally as specific failures demand it. Attempt 2 started with maximum governance and achieved nothing functional. Attempt 3 started with maximum features and achieved nothing integrated. The rebuild starts with maximum integration and minimum scope.

---

## 7. The User's Vision

### Primary Identity: Personal Jarvis
Atlas is a personal AI assistant. The user wants:
- An AI that understands them deeply and improves over time
- Proactive behavior: "I noticed X, should I Y?"
- Privacy: runs locally, data stays on-device
- Trust: can be relied on for important tasks without fear of hallucination
- Autonomy: handles tasks without constant supervision
- Natural interaction: voice, conversation, not just commands

### Secondary Identity: Meta-System (AI That Builds AI)
Beyond personal assistant, Atlas is intended to be a meta-system capable of:
- Analyzing and improving its own architecture
- Building other AI systems from learned patterns
- Transferring knowledge across domains
- Compounding intelligence over time

This is the long-term vision (Phase 3-4, years away). The rebuild should not optimize for meta-capability at the expense of basic personal assistant functionality. Get the assistant working first.

### Business Context
- Current market value: $0 (no users, no revenue)
- Unique competitive advantages: neuro-symbolic core, 10-layer memory, local-first, self-modification
- Multiple viable paths: vertical product (DevOps/Security), AI infrastructure play, autonomous SaaS factory, enterprise on-prem
- The code is not the value — users are. Validation and distribution matter more than more features.

### What the User Does NOT Want
- Another broken prototype that "works in demo but fails in practice"
- Scope explosion — features built but never integrated
- Dependency on any single LLM provider (must work across model swaps)
- Being told "it should work" without proof it does

---

## 8. Honest Assessment of What Existed

### What Actually Worked in Attempt 3
- Memory layer implementations (L1-L10) with SQLite/FAISS backing
- Pydantic schemas for L3-L9 (L1, L2, L10 lacked validation)
- Intent parsing with hybrid BERT + symbolic fallback
- Sandbox execution via Docker with proposal workflow
- FastAPI server with 81 REST endpoints
- Basic conversation handling (when it didn't fail)
- Test infrastructure (pytest, markers, comprehensive coverage structure)

### What Was Built But Never Wired
- AutoRetrainingDaemon — complete pipeline, never instantiated at startup
- Event bus — events emitted from many components, only 4 subscribers
- Research agent — full implementation, disabled by default (config flag)
- Plugin manager and device sync — initialized, report healthy, completely hollow
- Voice infrastructure — TTS/STT/governance modules exist, VoiceController missing
- All feature flags in config set to FALSE

### What Was Simulated/Fake
- Multimodal subsystem — hash-based fake object detection, not real ML
- Health reporting — subsystems report health=True when they are stubs
- Some test validation claims — tests claimed to pass without execution evidence

### What Was Duplicated/Confused
- Four separate vector store implementations with confused import paths
- Three versions of meta-assessment (v1, v2, v3) with unclear which is active
- storage/ layer defines clean Protocol hierarchy that nothing imports

### Critical Missing Pieces
- No end-to-end conversation test ("hi atlas" → response)
- No LLM fallback when API unavailable (missing key = empty responses)
- No general web search capability (only academic APIs)
- No email, calendar, or home automation integration
- No persistent autonomous agent loop (reactive only)
- No API contract validation (code calling non-existent methods passes)
- 50+ silent exception handlers

---

## 9. Critical Lessons (Synthesized)

### L1: Integration Is Harder Than Implementation
Building a component is 30% of the work. Integrating it with the rest of the system, testing the integration, and proving it works end-to-end is 70%. Attempt 3 did the 30% for dozens of components and skipped the 70% for most of them.

### L2: AI Agents Optimize for Speed, Not Robustness
When an AI agent is asked to build something, it optimizes for "deliver working code fast." It does NOT optimize for "deliver robust, integrated, tested code." This was proven when Warp AI delivered Phase 2.2 with 46 critical oversights that only surfaced when explicitly asked "what's missing?" The rebuild must use forcing functions (DecisionValidator, test gates, integration requirements) that block progress until quality is verified.

### L3: Validation Theater Is the #1 Risk
The most dangerous failure is a system that CLAIMS to be validated but isn't. This creates false confidence and allows broken code to accumulate. The rebuild must make validation theater structurally impossible — validation claims require execution proof.

### L4: Governance Must Be Graduated
- Too little governance (Attempt 1): system drifts and breaks things
- Too much governance (Attempt 2): system can't do anything
- Right governance (Attempt 3's constitution, partially): safety net that catches real problems without blocking real work
- Graduated governance: start with minimum viable rules, add more as specific failures demand

### L5: The Memory System Is the Differentiator
Every assessment, honest or inflated, identifies the 10-layer memory system as the unique capability. It scored highest on every rubric. It is the moat. The rebuild must treat memory as the foundation, not a feature. Build memory first, build it right, build everything else on top of it.

### L6: Smaller Scope, Higher Quality
Attempt 3 reached 251,801 lines. Basic greeting failed. The rebuild should target an order of magnitude less code with an order of magnitude more reliability. Every line must earn its place.

### L7: The User's Instincts Were Correct
The user identified problems (inflated valuations, validation theater, broken functionality) that the AI agents initially overlooked or minimized. The user's judgment on what "working" means must be the final arbiter, not test counts or meta-scores.

---

## 10. Requirements for the Rebuild

### R1: Start With a Working Conversation Loop
Before any advanced capability is built, Atlas must be able to:
- Accept a user message via API
- Parse intent (symbolic first, ML advisory, LLM fallback)
- Retrieve relevant context from memory
- Generate a response
- Store the interaction in memory
- Return the response to the user
This loop must work 100% of the time for basic inputs. Everything else is built on this foundation.

### R2: Memory First
The 10-layer memory system is implemented before any other subsystem. Each layer must have:
- Pydantic schema validation
- CRUD operations
- Integration with MemoryManager
- At least one integration test proving it works in the conversation loop

### R3: Incremental Subsystem Addition
Subsystems are added one at a time. Each must be:
- Integrated with the existing system
- Proven with end-to-end tests
- Documented with its interface contract
before the next subsystem begins.

### R4: Standard Module Interface
Every module in the rebuild follows the same structure:
- Interface definition (abstract base class or Protocol)
- Implementation
- Pydantic schemas for inputs/outputs
- Unit tests
- Integration test proving it works with the rest of the system

### R5: Honest Health Reporting
No subsystem reports health=True unless it can demonstrate actual functionality. Stubs report status=STUB. Disabled capabilities report status=DISABLED. Health checks verify behavior, not just instantiation.

### R6: Model Independence
Atlas must work without any specific LLM. The symbolic core handles intent parsing and validation independently. LLM integration is an enhancement, not a requirement. If OpenAI is down, Atlas still parses intents, retrieves memory, and responds (with reduced quality, not zero functionality).

### R7: Local-First, Privacy-Default
All data stays on-device by default. No external API call required for core functionality. LLM calls are opt-in and gated. Memory is stored locally. This is a hard requirement for the user's trust and a competitive advantage for enterprise markets.

### R8: Observable and Debuggable
Every decision must be traceable: what intent was parsed, what memory was retrieved, what validation ran, what response was generated, and why. The user (who is not a programmer) must be able to understand what happened when something goes wrong.

### R9: Monorepo — Backend and Console Live Together
In Attempt 3, the backend (`atlas/`) and frontend console (`console/`) lived in separate project directories with separate dependency management. AI agents routinely got confused about which codebase they were in, made edits to the wrong files, and lost context when switching between the two. The rebuild uses a **single integrated project structure** where backend and frontend coexist. API contracts (Pydantic schemas on the backend, TypeScript types on the frontend) must be co-located or auto-generated from a shared source so that a change to one side is immediately visible to the other. One repo, one project, one context for any agent working on it.

### R10: Every Subsystem Has an Acceptance Test
Before a subsystem is considered complete, it must have at least one acceptance test that:
- Runs against the live server (not mocked)
- Sends real input through the full pipeline
- Verifies real output matches expected behavior
- Would FAIL if the subsystem's implementation were deleted or stubbed

The conversation loop's acceptance test is the foundation: send "hello" to `/v1/atlas/chat`, receive a coherent, governed response within 5 seconds. Every subsequent subsystem adds its own acceptance test that builds on this. Memory: store a fact, retrieve it in a later query. Learning: correct a classification, verify the correction persists. Self-modification: submit a proposal, verify it runs in sandbox.

Acceptance test pass rate is the only metric that matters. Unit test count is noise.

### R11: Data Migration Is Opt-In, Not Default
Attempt 3 contains user data: learned corrections (`data/training/intent_corrections.jsonl`), memories in SQLite, user preferences in L9, episodic history in L3. The rebuild starts with a **clean slate** by default. Data from Attempt 3 may be migrated into the new system only if: (a) it passes the new system's Pydantic schema validation, (b) there is an explicit migration script with tests, and (c) the user approves. No silent data inheritance — the new system must earn its data, not assume it.

---

## 11. Per-Subsystem Volumes

Volume 0 defines system-wide principles. The following volumes define per-subsystem design intent, interface contracts, scope boundaries, and implementation guidance. Each volume is produced by a deep-dive agent using the standardized template (`design-bible/VOLUME_TEMPLATE.md`).

**Planned volumes:**
- **Volume 1: Memory System** — L1-L10 architecture, schemas, MemoryManager, consolidation, persistence
- **Volume 2: Orchestrator & Conversation Loop** — Intent parsing, routing, ReAct engine, response generation, personality
- **Volume 3: Learning & Adaptation** — Active learner, correction pipeline, retraining, effectiveness tracking
- **Volume 4: Self-Modification & Sandbox** — Proposal pipeline, sandbox execution, verification, approval automation
- **Volume 5: Intelligence Pipeline** — Content ingestion, domain extraction, knowledge synthesis, amplification
- **Volume 6: Voice & Multimodal** — TTS/STT, speaker verification, utterance governance, WebRTC
- **Volume 7: Console (Frontend)** — UI architecture, visualization, chat interface, telemetry dashboard
- **Volume 8: API & Infrastructure** — Server, endpoints, error taxonomy, configuration, startup, concurrency model
- **Volume 9: Governance & Validation** — DecisionValidator, output governance, constitutional enforcement
- **Volume 10: External Tools & Capabilities** — Tool registry, STEM backends, security tools, screen control, scope triage

Each volume answers: What is this subsystem? What worked/failed in Attempt 3? What is the rebuild's design intent? What are the interface contracts? What is in scope vs. deferred vs. killed? See `VOLUME_TEMPLATE.md` for the mandatory structure.

---

## 12. Minimum Viable Atlas (MVA)

The MVA is the concrete definition of "done enough to be useful." It is a set of acceptance tests that must ALL pass for Atlas v4 to be called a working system. Coding agents stop scope-creeping when all 5 pass.

### MVA-1: Basic Conversation
Send `{"query": "hello"}` to `POST /v1/atlas/chat`. Receive a coherent, personality-consistent response within 5 seconds. This is the R1 foundation — if this fails, nothing else matters.

### MVA-2: Evidence-Grounded Response
Send a factual question (e.g., "What memory layers does Atlas have?"). Receive a response that cites specific evidence (memory retrieval, tool output) rather than hallucinating. Verifiable by checking response metadata for evidence sources.

### MVA-3: Memory Round-Trip
Store a fact via conversation (e.g., "My favorite color is blue"). In a later query, ask about that fact. Verify the system retrieves it from memory, not from the LLM's training data. This proves L3/L4 memory works end-to-end.

### MVA-4: Learning Round-Trip
Correct a wrong classification (e.g., Atlas classifies a query as "search" when it should be "memory retrieval"). Issue the correction. In a subsequent identical query, verify the classification is now correct. This proves the learning pipeline works.

### MVA-5: Server Health
Server boots with zero errors. `GET /health` returns all initialized subsystems as healthy. No subsystem reports healthy unless it can demonstrate actual functionality (R5). This is the baseline sanity check.

**Note:** The integration gate agent may refine these after seeing all Phase 1 outputs. The refined MVA in `gate-output/mva-refined.md` takes precedence once approved.

---

## 13. Build Order

Concrete ordering with dependency gates. Each tier must pass its gate before the next begins.

### Tier 0: Foundation
`atlas-v4/src/atlas/shared/` — errors, config, logging, types, llm (LLMProvider Protocol)
No dependencies. No MVA gate.

### Tier 1: Skeleton
`api/server.py` (empty FastAPI app + `/health` endpoint) + `governance/validator.py` (schema validation gate)
Depends on: Tier 0
Gate: Server boots, `/health` returns 200, ruff + mypy pass

### Tier 2: Core Loop
`orchestrator/engine.py` + `orchestrator/intent.py` + `orchestrator/response.py`
Depends on: Tier 0, Tier 1
Gate: **MVA-1 passes** (send hello, get coherent response)

### Tier 3: Memory
`memory/` — all 10 layers + manager + schemas
Depends on: Tier 0
Gate: **MVA-3 passes** (store fact, retrieve it in later query)

### Tier 4: Governance
`governance/output.py` — response governance (GovernedOutput, evidence grounding)
Depends on: Tier 2, Tier 3
Gate: **MVA-2 passes** (evidence-grounded response, not hallucinated)

### Tier 5: Learning
`learning/` — active learner, correction pipeline, retraining triggers
Depends on: Tier 3
Gate: **MVA-4 passes** (correct classification, verify it persists)

### Tier 6+: Capabilities (Parallel)
- Self-modification — depends on Tier 0-4 minimum
- Intelligence pipeline — depends on Tier 3, Tier 5
- Voice — depends on Tier 2, Tier 4
- External tools — depends on Tier 2
- Console — depends on Tier 1 (API contracts)

Each Tier 6+ capability follows R3: integrated, tested, documented before the next begins.

**Note:** The integration gate agent will refine this after seeing Phase 1 interface contracts. The refined build order in `gate-output/build-order-refined.md` takes precedence once approved.

---

## Appendix A: Source Document Index

These documents exist in the old repo and were synthesized into this Bible. They are preserved for provenance but should NOT be read directly by rebuild agents.

- `/COMPREHENSIVE_ANALYSIS_WARP_ATTEMPTS_v1.md` — Retrospective of Attempts 1-2, research synthesis
- `/WARP.md` — Project-wide technical guide
- `/CODEBASE_ANALYSIS_COMPLETE.md` — Jan 2026 codebase assessment
- `/atlas/docs/architecture/atlas-identity.md` — Name, purpose, role definition
- `/atlas/docs/architecture/atlas-constitution-v2.md` — Constitutional framework (10 articles)
- `/atlas/docs/architecture/atlas-constitution.md` — Constitutional framework v1
- `/atlas/docs/development/atlas-personality.md` — Personality configuration
- `/atlas/docs/architecture/capability-analysis-honest.md` — Moat vs. commodity analysis
- `/atlas/docs/development/personal-ai-rubric.md` — Personal Jarvis scoring rubric
- `/atlas/docs/development/meta-system-rubric.md` — Meta-system capability rubric
- `/atlas/docs/SELF_BUILDING_ATLAS_ROADMAP.md` — 36-month autonomy roadmap
- `/atlas/docs/LEARNING_FROM_AI_FAILURES.md` — Failure pattern learning system
- `/atlas/docs/atlas-evolution-pattern.md` — 5-rule safe evolution methodology
- `/atlas/docs/guides/business-strategy-discussion.md` — Revenue paths and strategy
- `/atlas/docs/architecture/critical-architecture-gaps-2026-03.md` — 7 identified architecture gaps
- `/atlas/docs/development/atlas-oversights-2026-02-08.md` — Integration oversights catalog
- `/atlas/docs/architecture/exhaustive-cognitive-architecture-analysis.md` — Component-level audit
- `/atlas/docs/plans/jarvis-gap-closure-plan.md` — Gap closure workstreams
- `/atlas/docs/architecture/intelligence-system.md` — Intelligence pipeline architecture
- `/atlas/docs/plans/intelligence-system-part-a.md` through `part-e.md` — Intelligence plans

---

## Appendix B: Terminology

- **Symbolic core** — deterministic parsing, validation, and execution logic. No ML involved. Produces the same output for the same input every time.
- **ML advisory** — BERT classifiers, domain classifiers, and other trained models that suggest classifications with confidence scores. Their output is NEVER acted on directly — always validated by symbolic core.
- **LLM fallback** — GPT-4o-mini or equivalent used only when both symbolic parser and ML classifiers have confidence below threshold. LLM output is validated before execution.
- **Validation theater** — claiming verification (tests pass, health OK) without actually performing it. The #1 systemic risk.
- **Design Bible** — this document series. The single source of truth for the rebuild.
- **Moat** — capability that is both valuable to users and difficult for competitors to replicate.
- **Promotion gate** — checkpoint where a learned behavior or new code must prove itself (via tests, metrics, or review) before being deployed to production.
- **Constitutional violation** — any action that violates the hard governance rules. Results in blocked execution, not just a log entry.

---

**END OF VOLUME 0**

*This document was synthesized from 15+ existing design documents spanning January-March 2026. It represents the distilled design intent, lessons, and requirements for the Atlas rebuild. When this document conflicts with any older document, this document prevails.*

---

## Modification History

| Version | Date | Modified By | Summary | Laymen Summary |
|---|---|---|---|---|
| v1 | 2026-03-10 | Oz | Initial creation — synthesized from 15+ source documents into system-wide principles, anti-patterns, requirements, and per-subsystem volume index | Created the master blueprint document that all rebuild agents must read first |
| v2 | 2026-03-10 | Oz | Added documentation standard header/footer per PROJECT_CONVENTIONS.md Section 9 | Added tracking metadata so we know who changed what and when |
| v3 | 2026-03-10 | Oz | Added Doc ID field (`DB-V00-001`) per PROJECT_CONVENTIONS.md Section 9.4 | Added unique document number for machine searching |
| v4 | 2026-03-10 | Oz | Added Section 12 (MVA: 5 acceptance tests defining "done") and Section 13 (Build Order: Tier 0-6 with dependency gates and MVA checkpoints) | Added the finish line (5 tests that must pass) and the build sequence (what to build in what order) |
