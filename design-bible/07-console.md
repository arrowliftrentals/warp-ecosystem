# ATLAS Design Bible — Volume 7: Console (Frontend)

| Field | Value |
|---|---|
| **Doc ID** | `DB-V07-001` |
| **Name** | Volume 7: Console (Frontend) |
| **Purpose** | Design specification for the visual interface — chat, telemetry, 3D visualization, file exploration, and system monitoring |
| **Owner** | Design Bible / Volume 7 |
| **Status** | `draft` (scaffold — Part A pre-loaded, Part B awaiting distillation agent) |
| **Supersedes** | N/A |
| **Superseded by** | N/A |
| **Author** | Oz (Part A) / TBD distillation agent (Part B) |
| **Version** | v3 |
| **Created** | 2026-03-10 |
| **Last Modified** | 2026-03-10 |

---

## Part A: Context (Pre-loaded)

### A.1 Subsystem Identity
- **Volume 7: Console (Frontend)**
- **Purpose:** The visual interface for interacting with Atlas — chat, telemetry, 3D neural visualization, file exploration, and system monitoring. The user's window into Atlas's mind.
- **Rebuild phase:** Phase 5-6 (parallel with voice, after backend is stable). Console depends on backend API contracts being stable.

### A.2 Source Manifest

**Code files to read** (paths relative to `console/`):

*Core:*
- `src/App.tsx` — root application
- `src/main.tsx` — entry point
- `vite.config.ts` — build configuration
- `server/index.ts` — dev server

*Pages:*
- `src/pages/ConsolePage.tsx` — main console view
- `src/pages/Neural3DPage.tsx` — 3D visualization page
- `src/pages/Neural3DFullscreenPage.tsx`
- `src/pages/LayoutEditorPage.tsx` — layout customization
- `src/pages/SettingsPage.tsx`
- `src/pages/DebugSessionsPage.tsx`
- `src/pages/TestParticlesPage.tsx`

*Chat & interaction:*
- `src/components/ChatPanel.tsx` — chat interface
- `src/components/PromptInput.tsx` — user input
- `src/components/AgentResponsePanel.tsx` — agent response display
- `src/components/ThinkingProcess.tsx` — shows reasoning steps
- `src/components/ToolCallList.tsx` — tool call display
- `src/components/CommandPlanList.tsx`
- `src/components/FeedbackPrompt.tsx` — user feedback collection
- `src/components/MessageActions.tsx`

*Visualization:*
- `src/components/NeuralArchitecture3DHost.tsx`
- `src/components/NeuralArchitecture3DScene.tsx`
- `src/components/NeuralNetworkScene.tsx`
- `src/components/NeuralHUD.tsx` — heads-up display overlay
- `src/components/NeuralGraph.tsx`
- `src/components/NeuralNode.tsx`
- `src/components/NeuralEdge.tsx`
- `src/components/NeuralOrganismView.tsx`
- `src/components/BrainCanvas.tsx`
- `src/components/MiniBrainPreview.tsx`
- `src/components/Architecture3DView.tsx`
- `src/components/ArchitectureView.tsx`
- `src/components/ArchitectureViewV2.tsx`
- `src/components/ArchitectureAnalysisDashboard.tsx`
- `src/components/ArchitectureAnalysisDashboard.old.tsx`

*System views:*
- `src/components/MemoryView.tsx` — memory layer inspection
- `src/components/GoalsView.tsx` — goal tracking
- `src/components/TasksView.tsx` — task management
- `src/components/LearningView.tsx` — learning system view
- `src/components/SkillsView.tsx` / `SkillsList.tsx` / `SkillDetail.tsx`
- `src/components/MetaView.tsx` — meta-assessment
- `src/components/DiagnosticsView.tsx`
- `src/components/SecurityView.tsx`
- `src/components/SandboxView.tsx`
- `src/components/SimulationView.tsx`
- `src/components/DriftReviewView.tsx`
- `src/components/RecommendationsView.tsx`
- `src/components/SystemsView.tsx`
- `src/components/LogsView.tsx`
- `src/components/AttentionView.tsx`
- `src/components/AnalysisPanel.tsx`
- `src/components/CodeAnalysisDashboard.tsx`
- `src/components/BenchmarkLiveView.tsx`

*UI infrastructure:*
- `src/components/ConsoleProvider.tsx` — global state
- `src/components/Sidebar.tsx`
- `src/components/MainTabs.tsx`
- `src/components/StatusBar.tsx`
- `src/components/TabHeader.tsx`
- `src/components/DashboardGrid.tsx` / `DashboardView.tsx`
- `src/components/DraggableDashboard.tsx` / `DraggableCardContent.tsx`
- `src/components/ConsoleFileExplorer.tsx` / `FileExplorer.tsx` / `FileViewer.tsx`
- `src/components/SessionSelector.tsx` / `SessionInfo.tsx`
- `src/components/ThemeSelector.tsx`
- `src/components/MarkdownRenderer.tsx`
- `src/components/EnhancedCodeBlock.tsx`
- `src/components/Timeline.tsx`
- `src/components/PermanentProgressBar.tsx` / `ProgressIndicator.tsx`
- `src/components/TaskProgress.tsx`
- `src/components/ColorPalettePainter.tsx`
- `src/components/DependencyMatrix.tsx`
- `src/components/FreeformRow.tsx`
- `src/components/PatchList.tsx`
- `src/components/PatternDetail.tsx` / `PatternsList.tsx`
- `src/components/SimpleFix.tsx`
- `src/components/TestPlanList.tsx`
- `src/components/TerminalPanel.tsx`
- `src/components/ConsoleLogInterceptor.tsx`

*API clients:*
- `src/lib/atlasClient.ts` — main backend API client
- `src/lib/atlasConsoleClient.ts` — console-specific API
- `src/lib/atlasLearningClient.ts` — learning API
- `src/lib/atlasSkillsClient.ts` — skills API
- `src/lib/atlasProjectFs.ts` — project filesystem API
- `src/lib/api.ts` — base API utilities

*State & context:*
- `src/contexts/TelemetryContext.tsx` — real-time telemetry
- `src/contexts/HealthContext.tsx` — system health
- `src/contexts/ThemeContext.tsx` — theming
- `src/contexts/ThreeSceneContext.tsx` — 3D scene shared state

*Utilities:*
- `src/lib/types.ts` — TypeScript type definitions
- `src/lib/session.ts` — session management
- `src/lib/layoutConfig.ts` — layout configuration
- `src/lib/debugLogger.ts` — debug logging
- `src/lib/diagramUtils.ts` — diagram utilities
- `src/lib/testOutputParser.ts` — test result parsing
- `src/lib/voiceGovernance.ts` — client-side voice governance

**Documentation to read (in console/):**
- `console/WARP.md` (if exists)
- Any `.md` files in `console/`

**Documentation to read (in atlas/docs/):**
- `docs/development/console-integration.md`
- `docs/development/console-integration-status.md`
- `docs/guides/startup-ux-improvements.md`

### A.3 Context Brief

**What worked in Attempt 3:**
- VS Code-inspired dark theme
- React Three Fiber for 3D neural architecture visualization (50k+ particles)
- Real-time telemetry via WebSocket
- Interactive chat interface with streaming responses
- File explorer and code viewer
- Multiple system views (memory, goals, tasks, learning, etc.)
- Draggable dashboard with customizable layout

**What failed or was never wired:**
- Console lived in a separate folder — AI agents got confused switching contexts (R9 addresses this)
- No test suite for frontend
- Unclear which views actually worked vs. were just scaffolded
- Multiple architecture visualization versions (v1, v2, old) — duplication
- 80+ component files — likely scope explosion similar to backend

**What was simulated/fake:**
- Some dashboard views may display placeholder data rather than real backend data

**Relevant Volume 0 principles:**
- R9: Monorepo — backend and console live together
- R8: Observable and debuggable (console is the observability tool)
- P7: Smaller and working beats larger and broken
- A1: Feature factory (80+ components, unclear which are integrated)

### A.4 Known Failures & Warnings
1. **80+ components is scope explosion**: Same A1 pattern as backend. Aggressive triage needed.
2. **No frontend tests**: The console had zero tests. The rebuild should define a testing strategy.
3. **Tech stack decision**: Attempt 3 used Next.js 16 + React 19.2 + React Three Fiber + Tailwind. The distillation agent should evaluate if this stack is right for the rebuild or if simplification is warranted.
4. **API contract drift**: Console API clients (`atlasClient.ts`, etc.) may have drifted from backend endpoints. R9's shared API contracts address this.
5. **3D visualization complexity**: React Three Fiber with 50k+ instanced particles is impressive but complex. Determine if this is REBUILD (core experience) or DEFER (nice-to-have).

---

## Part B: Design Specification (Agent Fills Out)

### B.1 Subsystem Purpose (Rebuild)
*[To be filled by distillation agent]*

### B.2 Architecture Overview
*[To be filled by distillation agent]*

### B.3 Interface Contracts
*[To be filled by distillation agent]*

### B.4 Scope Triage
*[To be filled by distillation agent — every component in A.2 must get a REBUILD/DEFER/KILL verdict]*

### B.5 Technology Choices
*[To be filled by distillation agent]*

### B.6 Data Model
*[To be filled by distillation agent]*

### B.7 Error Handling
*[To be filled by distillation agent]*

### B.8 Testing Strategy
*[To be filled by distillation agent]*

### B.9 Configuration
*[To be filled by distillation agent]*

### B.10 Subsystem Lessons Learned
*[To be filled by distillation agent]*

### B.11 Discoveries
*[To be filled by distillation agent]*

### B.12 Oversight Self-Review
*[To be filled by distillation agent — MANDATORY before submission]*

### B.13 Design Quality Scorecard
*[To be filled by distillation agent — MANDATORY. Minimum passing score: 30/45]*

---

## Modification History

| Version | Date | Modified By | Summary | Laymen Summary |
|---|---|---|---|---|
| v1 | 2026-03-10 | Oz | Initial scaffold — Part A pre-loaded with source manifest (80+ component files, 6 API clients, 4 contexts, 8 libs), context brief, and 5 known failure warnings including scope explosion and zero frontend tests | Created the console/frontend analysis document with file lists and known problems for the analysis agent to investigate |
| v2 | 2026-03-10 | Oz | Added documentation standard header/footer per PROJECT_CONVENTIONS.md Section 9 | Added tracking metadata so we know who changed what and when |
| v3 | 2026-03-10 | Oz | Added Doc ID field (`DB-V07-001`) per PROJECT_CONVENTIONS.md Section 9.4 | Added unique document number for machine searching |
