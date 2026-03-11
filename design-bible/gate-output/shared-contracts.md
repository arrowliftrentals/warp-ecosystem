# Integration Gate — Shared Contracts

| Field | Value |
|---|---|
| **Doc ID** | `DB-G01-002` |
| **Name** | Phase 1 Shared Contracts |
| **Purpose** | Binding interface contracts that span volume boundaries — the cross-subsystem API surface for Phase 2 |
| **Owner** | Design Bible / Integration Gate |
| **Status** | `active` |
| **Supersedes** | N/A |
| **Superseded by** | N/A |
| **Author** | Integration Gate Agent |
| **Version** | v1 |
| **Created** | 2026-03-10 |
| **Last Modified** | 2026-03-10 |

---

## 1. Shared Pydantic Schemas (types crossing subsystem boundaries)

### 1.1 Memory-Domain Schemas (Provider: Vol 1, Consumers: Vol 2, 3, 4, 5, 8, 9)
Location: `atlas/memory/schemas.py`
- `WorkingMemoryItem`, `Message`, `BufferedEvent`, `ConversationMetadata` — L1/L2
- `Episode`, `EventType` — L3
- `Fact`, `FactSource`, `FactRelation`, `FactEvidence` — L4
- `Skill`, `SkillExecution`, `SkillImprovement` — L5
- `FocusState` — L6
- `StateSnapshot` — L7
- `Goal`, `Plan`, `Progress` — L8
- `UserProfile`, `Interaction` — L9
- `CommandEvidence`, `ValidationClaim`, `ValidationClaimType` — L4 (consumed by Vol 4 VerificationTracker)
- `OutcomeSignal`, `OutcomeType` — shared between Vol 1 and Vol 3

### 1.2 Governance Schemas (Provider: Vol 9, Consumers: Vol 2, 6, 7, 8)
Location: `atlas/governance/schemas.py`
- `GovernedOutput` — single egress schema for all user-facing text/voice
- `ExtractedClaim` — factual claim with type, status, grounding refs
- `EvidenceItem` — verbatim tool result with SHA256 integrity
- `EvidenceContract` — required evidence per intent pattern
- `AuthorityLevel` enum: GROUNDED, ADVISORY, SPECULATIVE
- `ClaimType` enum: QUANTITATIVE, EXISTENCE, CAPABILITY, CAUSAL, LOCATION, PROCEDURE, POLICY
- `ClaimStatus` enum: SUPPORTED, UNSUPPORTED, UNVERIFIABLE, SUBJECTIVE
- `OutputPhase` enum: THINK, OBSERVE_SUMMARY, REFLECT, ANSWER, COUNCIL_SYNTHESIS
- `ValidationDecision` — result of DecisionValidator (SAFE/UNSAFE/NEEDS_REVIEW/NEEDS_USER_INPUT)

### 1.3 API Contract Schemas (Provider: Vol 8, Consumers: Vol 7)
Location: `contracts/api_schemas.py`
- `ChatRequest` — `query: str`, `session_id: str | None`, `context: str | None`, `stream: bool = False`
- `ChatResponse` — `answer: str`, `session_id: str`, `evidence: list[EvidenceRef]`, `tool_calls: list[ToolCallSummary] | None`, `governed: bool`, `metadata: dict`
- `EvidenceRef` — `source: str`, `content_snippet: str`, `confidence: float`
- `ToolCallSummary` — `tool: str`, `status: str`, `result_summary: str | None`
- `ErrorResponse` — `error: str`, `detail: str`, `type: str`, `path: str`, `severity: str | None`, `request_id: str | None`
- `HealthResponse` — `status: str`, `service: str`, `version: str`, `subsystems: dict`, `uptime_seconds: float`

### 1.4 Learning-Domain Schemas (Provider: Vol 3, Consumers: Vol 2, 4, 5)
Location: `atlas/learning/schemas.py` (pending C-02 resolution)
- `NormalizedContent`, `ContentType` — knowledge pipeline input
- `DomainClassification`, `ScientificDomain` — domain routing
- `ExtractionResult`, `ExtractedEntity`, `ExtractedRelation` — extraction output
- `RefinedKnowledge`, `SynthesizedKnowledge` — knowledge pipeline output (consumed by Vol 5)
- `DomainKnowledgeEntry`, `ContradictionResult`, `ConflictType` — knowledge integrity
- `IntentCorrection` — correction record (consumed by Vol 2 feedback flow)

### 1.5 Intelligence-Domain Schemas (Provider: Vol 1 data / Vol 5 behavior, Consumers: Vol 2)
Location: `atlas/memory/schemas.py` (pending C-03 resolution)
- `StructuralAnalogy` — cross-domain analogies
- `Hypothesis` — testable hypotheses with falsification criteria
- `ResearchGap` — knowledge gaps
- `SocraticChallenge` — reasoning challenges
- `IntellectualProfile` — per-user growth tracking
- `CalibratedConfidence` — evidence-based confidence
- `ProvenanceChain`, `ProvenanceStep`, `SourceQuality` — provenance tracking

### 1.6 Orchestrator-Domain Schemas (Provider: Vol 2, Consumers: Vol 7, 8)
Location: `atlas/orchestrator/schemas.py`
- `UnifiedIntent` — `category`, `domain`, `confidence`, `action`, `target`, `entities`, `raw_command`, `needs_llm`, `classification_source`
- `ConversationResponse` — internal engine output (mapped to ChatResponse by Vol 8)
- `ConversationRequest` — `query`, `session_id`, `device_id`, `stream`
- `MemoryContext` — assembled context from memory layers
- `RawResponse` — pre-governance response with evidence store
- `PersonalityTraits` — immutable personality configuration

### 1.7 Self-Modification Schemas (Provider: Vol 4, Consumers: Vol 2, 3)
Location: `atlas/self_modify/schemas.py`
- `CodeChange` — file path, original/modified content, diff, rationale
- `ImprovementProposal` — proposal with validation status, risk level
- `ProposalStatus` enum: PENDING, APPLIED, REJECTED, ROLLED_BACK
- `RiskLevel` enum: LOW, MEDIUM, HIGH, CRITICAL
- `RiskAssessment` — 7-gate risk evaluation
- `ValidationTheaterIssue` — theater detection finding
- `ExecutionResult` — sandbox execution result

---

## 2. API Boundary Contracts (who calls what, exact signatures)

### 2.1 Vol 8 → Vol 2 (API routes call orchestrator)
```
ConversationEngine.process_message(message: str, session_id: str, device_id: str) -> ConversationResponse
```
Vol 8 route handler maps ChatRequest → process_message args, maps ConversationResponse → ChatResponse.

### 2.2 Vol 2 → Vol 1 (Orchestrator calls memory)
```
MemoryManager.start_conversation(conversation_id: str, device_id: str) -> ConversationState
MemoryManager.add_message(conversation_id: str, role: str, content: str, metadata: dict | None) -> None
MemoryManager.get_recent_messages(conversation_id: str, limit: int) -> list[dict]
MemoryManager.assemble_context(conversation_id: str, user_query: str | None, max_messages: int, max_facts: int, max_episodes: int, max_semantic: int) -> dict
MemoryManager.end_conversation(conversation_id: str) -> None
MemoryManager.get_stats() -> dict
MemoryManager.get_recent_conversations(hours: int, limit: int) -> list[dict]
```

### 2.3 Vol 2 → Vol 9 (Orchestrator calls governance)
```
DecisionValidator.validate(command: str, bert_result) -> ValidationDecision
DecisionValidator.validate_intent(intent, context) -> ValidationDecision
DecisionValidator.validate_tool_execution(tool_name: str, args: dict, context: dict) -> ValidationDecision
AnswerGovernor.govern(content: str, phase: OutputPhase, evidence_store: EvidenceStore) -> GovernedOutput
```

### 2.4 Vol 2 → Vol 10 (Orchestrator calls tools)
```
ToolRegistry.execute(tool_name: str, arguments: dict, context: dict | None) -> ToolResult
ToolRegistry.get_openai_schema_for_query(query: str, max_tools: int) -> list[dict]
```

### 2.5 Vol 2 → Vol 3 (Orchestrator calls learning)
```
LearningManager.suggest_patterns(trigger: str, context: dict | None, limit: int) -> list[dict]
OutcomeDetector.analyze_follow_up(previous_query, previous_response, follow_up_message, provenance, conversation_id) -> OutcomeSignal
```

### 2.6 Vol 2 → Vol 5 (Orchestrator calls intelligence)
```
IntelligenceCoordinator.amplify_query(query: str, user_id: str, domain: str | None) -> AmplificationResult
IntelligenceCoordinator.cross_domain_insight(concept, source_domain, target_domain, user_id) -> CrossDomainResult
IntelligenceCoordinator.challenge_and_refine(claim: str, user_id: str, context: str | None) -> ChallengeResult
```

### 2.7 Vol 9 → Vol 2 (Governance needs tool results)
```
EvidenceStore.store(tool_name: str, args: dict, result: Any) -> EvidenceItem
```
Vol 2 calls this after each tool execution in the ReAct loop, before calling AnswerGovernor.govern().

### 2.8 Vol 6 → Vol 2 (Voice calls orchestrator)
```
OrchestratorEngine.process_message(message: str, session_id: str, device_id: str) -> ConversationResponse
```
Via VoiceController; same interface as Vol 8.

### 2.9 Vol 4 → Vol 1 (Self-modification stores claims)
```
MemoryManager.l4.store_fact(content, source, confidence, metadata) -> str
MemoryManager.l4.query_facts(query, min_confidence, limit) -> list[DeclarativeFact]
```

### 2.10 Vol 4 → Vol 9 (Self-modification validates intents)
```
DecisionValidator.validate_intent(intent: str, context: dict) -> ValidationDecision
```

### 2.11 Vol 3 → Vol 1 (Learning accesses memory)
```
MemoryManager.l3.store_episode(Episode) -> None
MemoryManager.l4.search_facts(query, limit) -> list[dict]
MemoryManager.l5.store_skill(Skill) -> None
MemoryManager.l7 (world state capture/query)
MemoryManager.l10 (vector search)
```

### 2.12 Vol 10 → Vol 1 (Tools access memory)
```
MemoryManager with layer accessors (.l1 through .l10), search methods, get_stats()
```

### 2.13 Vol 10 → Vol 9 (Tools validate dangerous operations)
```
DecisionValidator.validate(command: str, context: dict | None) -> ValidationResult
```

### 2.14 Vol 7 → Vol 8 (Console calls API)
All HTTP endpoints listed in Vol 7 B.3.1 (chat, sessions, memory, health, tasks, goals).
SSE streaming via `POST /v1/atlas/chat` with `stream: true`.
WebSocket: `ws://host/ws/telemetry`.

---

## 3. Memory Layer Interface (how each subsystem interacts with memory)

All access through `MemoryManager` facade — no direct layer imports.

- **Vol 2 (Orchestrator):** L1 (session state), L3 (episode logging), L4 (fact retrieval), L5 (skills), L8 (goals), L9 (user profile), L10 (semantic search). Primary consumer via `assemble_context()`.
- **Vol 3 (Learning):** L3 (episode storage), L4 (fact assertion/search), L5 (procedural patterns/corrections), L7 (world state for trigger detection), L10 (semantic dedup).
- **Vol 4 (Self-Modification):** L4 (validation claim storage/query), L7 (execution proof storage).
- **Vol 5 (Intelligence):** L4 (fact queries for hypothesis/analogy), L9 (user profile for growth tracking), L10 (semantic search for analogy discovery), L3 (episode storage for challenge resolutions).
- **Vol 6 (Voice):** L3 (voice interaction episode logging).
- **Vol 8 (API):** `get_stats()`, `get_recent_conversations()` for health/admin endpoints.
- **Vol 9 (Governance):** L4 (fact search for evidence grounding).
- **Vol 10 (Tools):** Full layer access through MemoryTools handler.

---

## 4. Event/Message Contracts

No formal event bus is defined in the MVA rebuild. Vol 6 (Voice) references EventBus publication (`voice.query.processed`) and Vol 7 (Console) references WebSocket telemetry, but neither defines a formal event schema contract.

**Recommendation for Phase 2:** If an event bus is needed, define a base `AtlasEvent` Pydantic schema in `shared/types.py` with `event_type: str`, `timestamp: datetime`, `payload: dict`. Subsystems register event types. Vol 8 owns the transport (WebSocket broadcast). This is NOT blocking for Phase 2 — defer until Tier 4+.

---

## 5. Shared Infrastructure Contracts

### 5.1 Error Hierarchy (Provider: Vol 8 / shared, Consumers: all)
Location: `atlas/shared/errors.py`
- `AtlasError(Exception)` — base with `category`, `severity`, context dict
- `ValidationError`, `MemoryLayerError`, `GovernanceViolation`, `IntentParsingError`, `LLMProviderError`, `ToolExecutionError`, `SandboxError`, `ConfigurationError`

### 5.2 Configuration (Provider: Vol 8 / shared, Consumers: all)
Location: `atlas/shared/config.py`
- `AtlasConfig(BaseSettings)` — env prefix `ATLAS_`, flat structure, feature flags default OFF

### 5.3 Logging (Provider: shared, Consumers: all)
Location: `atlas/shared/logging.py`
- `structlog.get_logger()` — structured JSON logging

### 5.4 LLM Provider Abstraction (Provider: shared, Consumers: Vol 2, 3)
Location: `atlas/shared/llm.py`
- `LLMProvider` Protocol — model-independent interface for LLM calls (R6)

---

## Modification History

| Version | Date | Modified By | Summary | Laymen Summary |
|---|---|---|---|---|
| v1 | 2026-03-10 | Integration Gate Agent | Initial creation — synthesized interface contracts from all 10 volumes into 5 sections: shared schemas, API boundaries, memory layer access, event contracts, and shared infrastructure | Created the master contract document that all subsystem rebuild agents must follow |
