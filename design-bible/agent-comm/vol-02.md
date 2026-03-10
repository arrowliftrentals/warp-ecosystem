# Agent Communication — Volume 2: Orchestrator & Conversation Loop

> **Rules:** Append new claims/dependencies/conflicts using the formats defined in `AGENT_COMM.md`.
> This file is the ONLY place Vol 2 agents register changes. Do NOT edit `AGENT_COMM.md` directly.

---

## Ownership Claims

```
CLAIM: BERT classification schema (BertClassificationResult)
OWNER: Volume 2 (currently in src/memory/schemas.py, must move in rebuild)
REASON: Intent classification belongs to the orchestrator pipeline, not memory.
CONTESTED: no
```

---

## Dependency Declarations

```
DEPENDENCY: Volume 2 (Orchestrator) needs MemoryManager.assemble_context() from Volume 1
STATUS: pending
INTERFACE: assemble_context(conversation_id: str, user_query: Optional[str], max_messages: int = 10, max_facts: int = 5, max_episodes: int = 3, max_semantic: int = 5) -> Dict[str, Any]
```

```
DEPENDENCY: Volume 2 (Orchestrator) needs ToolRegistry.execute() and ToolRegistry.get_openai_schema_for_query() from Volume 10
STATUS: pending
INTERFACE: ToolRegistry.execute(tool_name, arguments, context) -> ToolResult; ToolRegistry.get_openai_schema_for_query(query, max_tools) -> list[dict]
```

```
DEPENDENCY: Volume 2 needs LearningManager.suggest_patterns() from Volume 3
STATUS: pending
INTERFACE: suggest_patterns(trigger: str, context: dict | None, limit: int) -> list[dict] with keys trigger, action, confidence, type
```

```
DEPENDENCY: Volume 2 needs OutcomeDetector.analyze_follow_up() from Volume 3
STATUS: pending
INTERFACE: async analyze_follow_up(previous_query, previous_response, follow_up_message, provenance, conversation_id) -> OutcomeSignal
```

```
DEPENDENCY: Volume 2 needs SelfModifier.propose_improvement() from Volume 4
STATUS: pending
INTERFACE: async propose_improvement(title, description, changes, progress_callback) -> ImprovementProposal
```

```
DEPENDENCY: Volume 2 (Orchestrator) needs IntelligenceCoordinator.amplify_query(), cross_domain_insight(), challenge_and_refine() from Volume 5
STATUS: pending
INTERFACE: IntelligenceCoordinator methods as specified in Volume 5 B.3
```

```
DEPENDENCY: Volume 2 (Orchestrator) needs AnswerGovernor.govern() from Volume 9
STATUS: pending
INTERFACE: AnswerGovernor.govern(content: str, phase: OutputPhase, evidence_store: EvidenceStore) → GovernedOutput
```

```
DEPENDENCY: Volume 2 (Orchestrator) needs DecisionValidator.validate_tool_execution() from Volume 9
STATUS: pending
INTERFACE: DecisionValidator.validate_tool_execution(tool_name: str, args: dict, context: dict) → ValidationDecision
```

---

## Conflict Acknowledgements

```
CONFLICT: Chat endpoint request field naming
VOLUMES: 8 vs 2 vs 7
RESOLUTION: resolved — Field name is 'query' everywhere (conflict-report.md C-12)
```
