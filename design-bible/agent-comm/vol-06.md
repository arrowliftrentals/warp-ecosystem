# Agent Communication — Volume 6: Voice & Multimodal
## Phase 2 Distillation Outputs

---

## Ownership Claims

```
CLAIM: VoiceController (controller.py) — core STT→Atlas→TTS pipeline orchestrator
OWNER: Volume 6
REASON: Central voice subsystem component. Consumes orchestrator, governance, memory.
CONTESTED: no
```

```
CLAIM: TTSEngine Protocol and PiperTTSEngine implementation (tts.py, piper_tts.py)
OWNER: Volume 6
REASON: Local ONNX TTS engine is voice-domain infrastructure.
CONTESTED: no
```

```
CLAIM: STTEngine Protocol (stt.py)
OWNER: Volume 6
REASON: Speech-to-text interface definition. No default implementation in rebuild.
CONTESTED: no
```

```
CLAIM: TextNormalizer (text_normalizer.py)
OWNER: Volume 6
REASON: TTS-specific text preprocessing. Pure string transforms.
CONTESTED: no
```

```
CLAIM: Voice Pydantic schemas (voice/schemas.py)
OWNER: Volume 6
REASON: All schemas serve voice subsystem exclusively.
CONTESTED: no
```

```
CLAIM: Voice API route definitions (/v1/voice/*)
OWNER: Volume 6 (definitions); Volume 8 (registration and hosting)
REASON: Vol 6 defines route handlers. Vol 8 registers the APIRouter.
CONTESTED: no
```

```
CLAIM: VoiceTools (tools/voice.py) — speak(), transcribe(), get_voice_status()
OWNER: Volume 6 (implementation); Volume 10 (registration)
REASON: Vol 6 implements voice tool handlers. Vol 10 registers in ToolRegistry.
CONTESTED: no
```

---

## Dependency Declarations

```
DEPENDENCY: Volume 6 needs OrchestratorEngine from Volume 2
STATUS: pending
INTERFACE: OrchestratorEngine.process_message(message, session_id, device_id) -> ConversationResponse
NOTE: B.3 incorrectly uses process_query. Must align with shared-contracts.md §2.8.
```

```
DEPENDENCY: Volume 6 needs GovernedOutput and OutputGovernor from Volume 9
STATUS: pending
INTERFACE: OutputGovernor.govern(content, phase, evidence_store) -> GovernedOutput
NOTE: Replaces Attempt 3 ApprovedUtterance. Per C-14 (resolved).
```

```
DEPENDENCY: Volume 6 needs DecisionValidator from Volume 9
STATUS: pending
INTERFACE: DecisionValidator.validate(command, bert_result) -> ValidationDecision
NOTE: Gates voice query safety before orchestrator processing.
```

```
DEPENDENCY: Volume 6 needs MemoryManager.l3 from Volume 1
STATUS: pending
INTERFACE: MemoryManager.l3.record_episode(event_type, session_id, context, outcome, importance)
NOTE: Logs VoiceInteractionEpisode to L3 episodic memory. Non-blocking.
```

```
DEPENDENCY: Volume 6 needs AtlasError from shared/errors.py (Volume 8)
STATUS: pending
INTERFACE: class AtlasError(Exception) — base for VoiceSubsystemError hierarchy.
```

```
DEPENDENCY: Volume 6 needs AtlasConfig from shared/config.py (Volume 8)
STATUS: pending
INTERFACE: AtlasConfig(BaseSettings) with env_prefix=ATLAS_. Voice reads 8 config fields.
```

```
DEPENDENCY: Volume 6 needs structlog from shared/logging.py (cross-cutting)
STATUS: pending
INTERFACE: from atlas.shared.logging import get_logger -> structlog.BoundLogger
```

```
DEPENDENCY: Volume 6 needs API route registration from Volume 8
STATUS: pending
INTERFACE: Vol 8 includes Vol 6 APIRouter via app.include_router(voice_router).
```

```
DEPENDENCY: Volume 6 needs tool registration from Volume 10
STATUS: pending
INTERFACE: ToolRegistry.register(tool_name, handler, schema) for speak, transcribe, get_voice_status.
```

---

## Conflict Flags

```
CONFLICT: B.3 method name mismatch with shared-contracts.md
VOLUMES: 6 vs shared-contracts
DESCRIPTION: B.3 uses process_query but shared-contracts.md defines process_message. Shared contract is binding.
RESOLUTION: Vol 6 uses process_message. Phase 1 documentation error.
STATUS: acknowledged
```

```
CONFLICT ACKNOWLEDGEMENT: C-09 (TTS/STT Voice Logic in Console — Vol 6 vs Vol 7)
VOLUMES: 6 vs 7
DESCRIPTION: Vol 7 identified ChatPanel.tsx inlines voice logic that belongs to Vol 6.
RESOLUTION: Vol 6 owns TTS/STT backend. Vol 7 consumes Vol 6 REST API. Cloud TTS proxies DEFER’d.
STATUS: acknowledged
```

```
CONFLICT ACKNOWLEDGEMENT: C-14 (GovernedOutput supersedes ApprovedUtterance — Vol 6 vs Vol 9)
VOLUMES: 6 vs 9
DESCRIPTION: Resolved. GovernedOutput is the single egress schema. Vol 6 KILLs governance.py.
STATUS: resolved
```

---

## Discoveries for Other Volumes

**For Volume 0:** Egress governance pattern candidate for P12. Lazy model loader standardization. Apple Silicon OpenMP guard.

**For Volume 2:** VoiceController calls process_message per shared-contracts.md. Voice queries identical to text queries.

**For Volume 7:** Cloud TTS proxy endpoints DEFER’d. Vol 7 may implement thin proxies if needed.

**For Volume 8:** AtlasError base class is Tier 0 dependency. AtlasConfig needed. Voice routes registered as APIRouter.

**For Volume 9:** Vol 6 consumes GovernedOutput and DecisionValidator.

**For Volume 10:** VoiceTools must be registered in ToolRegistry.

---

## Phase 2 B.4 Verdict Amendment

No changes. All REBUILD/DEFER/KILL decisions confirmed by Phase 2 source reading.

---

## Modification History

| Version | Date | Modified By | Summary |
|---|---|---|---|
| v1 | 2026-03-11 | Distillation Agent V6 (Phase 2) | Initial creation — 7 ownership claims, 9 dependency declarations, 3 conflict flags, 6 cross-volume notifications, 0 B.4 amendments |
