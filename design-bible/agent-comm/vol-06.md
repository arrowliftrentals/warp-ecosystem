# Agent Communication — Volume 6: Voice & Multimodal

> **Rules:** Append new claims/dependencies/conflicts using the formats defined in `AGENT_COMM.md`.
> This file is the ONLY place Vol 6 agents register changes. Do NOT edit `AGENT_COMM.md` directly.

---

## Ownership Claims

```
CLAIM: VoiceController (STT→Atlas→TTS pipeline orchestration, voice session management)
OWNER: Volume 6
REASON: Central voice subsystem coordinator. Manages voice sessions, delegates to STT/TTS engines, integrates with governance and memory.
CONTESTED: no
```

```
CLAIM: TTSEngine Protocol + PiperTTSService + XTTSTTSService (text-to-speech layer)
OWNER: Volume 6
REASON: TTS engine implementations and pluggable protocol for voice output. Piper (local-first R7), XTTS (higher quality, deferred).
CONTESTED: no
```

```
CLAIM: STTEngine (speech-to-text input layer)
OWNER: Volume 6
REASON: STT engine protocol and implementations (macOS SFSpeechRecognizer stub, cloud proxies). Vol 6 owns backend STT; Vol 7 owns browser-side recording UI.
CONTESTED: no
```

```
CLAIM: TextNormalizer (TTS text preprocessing)
OWNER: Volume 6
REASON: Pure-function text transforms for natural TTS output (numbers, units, acronyms, percentages). Zero external deps.
CONTESTED: no
```

```
CLAIM: SpeakerVerifier (voiceprint enrollment and verification)
OWNER: Volume 6
REASON: Resemblyzer GE2E embeddings, encrypted voiceprints, liveness heuristic. Deferred but design owned by Vol 6.
CONTESTED: no
```

```
CLAIM: Voice API routes (/v1/voice/*)
OWNER: Volume 6 (endpoint definition); Volume 8 (endpoint registration/infrastructure)
REASON: Vol 6 defines WHAT voice endpoints exist and their behavior. Vol 8 defines HOW they are registered in FastAPI.
CONTESTED: no
```

```
CLAIM: VoiceTools (LLM-callable speak/transcribe/get_voice_status)
OWNER: Volume 6 (tool logic); Volume 10 (tool registry infrastructure)
REASON: Voice tool implementations owned by Vol 6. Registration in ToolRegistry owned by Vol 10.
CONTESTED: no
```

---

## Dependency Declarations

```
DEPENDENCY: Volume 6 (Voice) needs GovernedOutput from Volume 9 to replace ApprovedUtterance
STATUS: pending
INTERFACE: GovernedOutput schema (replaces ApprovedUtterance for all output modalities including voice)
```

```
DEPENDENCY: Volume 6 (Voice) needs DecisionValidator.validate() from Volume 9 for query safety gating
STATUS: pending
INTERFACE: DecisionValidator.validate(command: str) -> ValidationDecision
```

```
DEPENDENCY: Volume 6 (Voice) needs API endpoint registration from Volume 8
STATUS: pending
INTERFACE: FastAPI router registration for /v1/voice/* endpoints
```

```
DEPENDENCY: Volume 6 (Voice) needs MemoryManager.l3.record_episode() from Volume 1 for voice interaction logging
STATUS: pending
INTERFACE: MemoryManager.l3.record_episode(episode: Episode) -> None
```

```
DEPENDENCY: Volume 6 (Voice) needs OrchestratorEngine.process_query() from Volume 2
STATUS: pending
INTERFACE: OrchestratorEngine.process_query(query: str, session_id: str) -> str
```

```
DEPENDENCY: Volume 6 (Voice) needs ToolRegistry registration from Volume 10 for VoiceTools
STATUS: pending
INTERFACE: ToolRegistry.register(tool_definition: ToolDefinition)
```

---

## Conflict Acknowledgements

```
CONFLICT: TTS/STT voice logic inlined in Console ChatPanel.tsx
VOLUMES: 7 vs 6
RESOLUTION: resolved — Vol 6 owns TTS/STT implementation. Vol 7 extracts inlined voice code and consumes a clean interface from Vol 6 (conflict-report.md C-09)
```

```
CONFLICT: GovernedOutput supersedes ApprovedUtterance
VOLUMES: 6 vs 9
RESOLUTION: resolved — GovernedOutput (Vol 9) replaces ApprovedUtterance. Vol 6 consumes GovernedOutput for voice output (conflict-report.md)
```
