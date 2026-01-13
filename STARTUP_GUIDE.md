# WARP Ecosystem Startup Guide

**Last Updated**: January 13, 2026  
**Configuration**: Phase 2+ (Neuro-Symbolic Hybrid)

---

## Project Structure

```
/Users/mac_m3/Projects/WARP Ecosystem/
├── atlas/                    # Backend (FastAPI - Neuro-Symbolic Hybrid)
├── console/                  # Frontend (Next.js Web Console)
├── STARTUP_GUIDE.md         # This file
├── ATLAS_PHASE1_IMPLEMENTATION_PLAN.md
└── COMPREHENSIVE_ANALYSIS_WARP_ATTEMPTS_v1.md
```

---

## Quick Start (Both Servers)

### Option 1: Global Command (Recommended)

The easiest way to start the entire WARP Ecosystem:

```bash
run_atlas
```

This single command will:
1. Start the backend server on port 8000
2. Start the frontend server on port 3000
3. Wait for both to initialize
4. Automatically open http://localhost:3000 in your browser

**Other Options:**
```bash
run_atlas -b           # Start only backend
run_atlas -f           # Start only frontend
run_atlas -s           # Stop all servers
run_atlas -r           # Restart all servers
run_atlas -l           # View logs in real-time
run_atlas -h           # Show help
```

---

### Option 2: Manual Startup

#### Terminal 1: Start Backend
```bash
cd "/Users/mac_m3/Projects/WARP Ecosystem/atlas"
python3 -m uvicorn src.api.server:app --host 127.0.0.1 --port 8000 --reload
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using WatchFiles
INFO:     Started server process [xxxxx]
INFO:     Application startup complete.
```

**Health Check:**
```bash
curl -s http://127.0.0.1:8000/health | jq
```

---

### Terminal 2: Start Frontend
```bash
cd "/Users/mac_m3/Projects/WARP Ecosystem/console"
npm run dev
```

**Expected Output:**
```
▲ Next.js 16.0.10 (Turbopack)
- Local:         http://localhost:3000
- Network:       http://192.168.x.x:3000

✓ Starting...
✓ Ready in XXXms
```

**Open Console:**
```bash
open http://localhost:3000
```

---

## Backend Details

**Location:** `/Users/mac_m3/Projects/WARP Ecosystem/atlas/`

**Architecture:** Neuro-Symbolic Hybrid (Attempt 3)
- Symbolic Core: Deterministic parsing and logic for reliability
- LLM Fallback: Flexible handling when symbolic methods have low confidence
- Confidence Threshold: < 0.5 triggers LLM fallback

**Technology Stack:**
- Framework: FastAPI
- Language: Python 3.11+
- Database: PostgreSQL (structured), ChromaDB (vectors)
- AI/ML: OpenAI API (GPT-4, GPT-4o-mini)

**Key Endpoints:**
- `/health` - Health check with subsystem status
- `/api/console/sessions` - Session management
- `/v1/atlas/chat` - Main chat endpoint
- `/v1/atlas/logs` - Activity logs
- `/v1/atlas/skill/executions` - Command execution history
- `/v1/telemetry/stream` - WebSocket telemetry stream
- `/v1/telemetry/bottlenecks` - Performance bottlenecks
- `/v1/telemetry/hot-paths` - Most used paths
- `/v1/telemetry/critical-paths` - High criticality paths
- `/v1/telemetry/flows` - Recent flows
- `/v1/telemetry/error-edges` - Error visualization
- `/v1/architecture/graph` - Architecture graph data
- `/api/sandbox/execute` - Sandbox command execution

**Environment:**
- Requires `.env` file with `OPENAI_API_KEY` and Pinecone configuration
- Located at: `/Users/mac_m3/Projects/WARP Ecosystem/atlas/.env`

---

## Frontend Details

**Location:** `/Users/mac_m3/Projects/WARP Ecosystem/console/`

**Architecture:** Next.js 16 Web Console with VS Code-style interface

**Technology Stack:**
- Framework: Next.js 16 (App Router)
- React: v19.2
- 3D Graphics: React Three Fiber (@react-three/fiber, @react-three/drei)
- Styling: Tailwind CSS
- State Management: Zustand (telemetry), React Context (console/session)
- Graph Visualization: Cytoscape.js with Reactflow

**Key Features:**
- Real-time 3D neural network visualization
- Interactive chat interface with streaming responses
- File explorer and code viewer
- Telemetry and observability displays
- Architecture graph visualization
- Cognitive region classification (Core/Memory/Perception)
- Particle flow animations

**Development Commands:**
```bash
npm run dev      # Start dev server (port 3000)
npm run build    # Build for production
npm run start    # Start production server (requires build first)
npm run lint     # Run linter
```

**API Proxy Configuration:**
- Frontend proxies API requests to backend at `http://localhost:8000`
- Configurable via `NEXT_PUBLIC_ATLAS_API_URL` environment variable
- API routes in `app/api/` handle proxy logic

---

## Session Management

**Session Storage:**
- Backend stores sessions in memory system (L1/L2)
- Frontend stores active session ID in localStorage
- Sessions persist across page refreshes

**Session Endpoints:**
- `GET /api/console/sessions` - List all sessions
- `POST /api/console/sessions` - Create new session
- `POST /api/console/sessions/{id}/clear` - Clear session history

**Clearing Sessions:**
If sessions appear stale, clear localStorage in browser console:
```javascript
localStorage.clear();
location.reload();
```

---

## Background Server Mode

### Start Both Servers in Background
```bash
# Backend
cd "/Users/mac_m3/Projects/WARP Ecosystem/atlas"
python3 -m uvicorn src.api.server:app --host 127.0.0.1 --port 8000 --reload > /tmp/warp-backend.log 2>&1 &

# Frontend
cd "/Users/mac_m3/Projects/WARP Ecosystem/console"
npm run dev > /tmp/warp-frontend.log 2>&1 &

# Open console
open http://localhost:3000
```

### Check Logs
```bash
tail -f /tmp/warp-backend.log
tail -f /tmp/warp-frontend.log
```

### Stop Servers
```bash
# Stop backend
pkill -f "uvicorn src.api.server:app"

# Stop frontend
pkill -f "next dev"
```

---

## Troubleshooting

### Backend Not Starting
**Check environment variables:**
```bash
cat "/Users/mac_m3/Projects/WARP Ecosystem/atlas/.env"
```

**Required variables:**
- `OPENAI_API_KEY`
- Pinecone configuration (if using vector store)

### Frontend Can't Connect to Backend
**Verify backend is running:**
```bash
curl -s http://127.0.0.1:8000/health
```

**Check API proxy configuration:**
```bash
grep -r "NEXT_PUBLIC_ATLAS" "/Users/mac_m3/Projects/WARP Ecosystem/console"
```

### Sessions Not Loading
**Test sessions endpoint:**
```bash
curl -s http://127.0.0.1:8000/api/console/sessions | jq
```

**Clear browser localStorage:**
1. Open browser console (F12)
2. Run: `localStorage.clear(); location.reload();`

### Port Already in Use
**Check what's using port 8000:**
```bash
lsof -ti:8000
```

**Kill process on port:**
```bash
kill $(lsof -ti:8000)
```

**Same for port 3000:**
```bash
kill $(lsof -ti:3000)
```

---

## Git Branches & Versions

### Backend (atlas)
- **Main Branch**: Production-ready (Phase 2 complete)
- **Last Commit**: 2026-01-10
- **Tests**: 116/117 passing (99.1%)

### Frontend (console)
- **Main Branch**: Latest features (Phase 3 particle animations)
- **Last Commit**: 2026-01-12
- **Phase 2 Baseline**: Commit `e60c90c8` (Phase 2: Advanced Console Integration)
- **Phase 3 Work**: 10 commits after Phase 2 (particle animations, debugging)

**To checkout Phase 2 baseline:**
```bash
cd "/Users/mac_m3/Projects/WARP Ecosystem/console"
git checkout e60c90c8
```

**To return to latest:**
```bash
cd "/Users/mac_m3/Projects/WARP Ecosystem/console"
git checkout main
```

---

## Related Projects (NOT in WARP Ecosystem)

### WARP-atlas (Experimental)
**Location:** `/Users/mac_m3/Projects/WARP-atlas`  
**Status:** Experimental "vNext" approach  
**Description:** Mission-driven, pure symbolic, anti-drift focus  
**Last Update:** 2026-01-08  
**Note:** Not used with current console, kept for evaluation

### WARP - Attempt 1 Atlas (Deprecated)
**Location:** `/Users/mac_m3/Projects/WARP - Attempt 1 Atlas`  
**Status:** Deprecated reference implementation  
**Description:** LLM-centric approach (suffered from drift issues)  
**Last Update:** 2025-12-15  
**Note:** Reference only, do not use for active development

---

## Phase History

### Phase 1: Infrastructure (COMPLETE)
- Sandbox system (VM management)
- Screen interaction (macOS Accessibility API)
- Self-modification capability
- Device presence (multi-device coordination)

### Phase 2: Intelligence (COMPLETE)
- Intent parser (deterministic + LLM fallback)
- Memory system (L1/L2 architecture)
- Learning engine (pattern recognition)
- Telemetry tracking (bottlenecks, hot paths)
- 3D neural visualization
- Architecture graph with cognitive regions

### Phase 3: Advanced Features (IN PROGRESS)
- Particle flow animations
- Real-time telemetry visualization
- Enhanced debugging tools
- Performance profiling

---

## Quick Reference Commands

```bash
# Start everything (recommended)
run_atlas

# Stop everything
run_atlas -s

# Restart everything
run_atlas -r

# View logs
run_atlas -l

# Start manually (if needed)
cd "/Users/mac_m3/Projects/WARP Ecosystem/atlas" && python3 -m uvicorn src.api.server:app --host 127.0.0.1 --port 8000 --reload &
cd "/Users/mac_m3/Projects/WARP Ecosystem/console" && npm run dev &
open http://localhost:3000

# Health checks
curl -s http://127.0.0.1:8000/health | jq
curl -s http://127.0.0.1:8000/api/console/sessions | jq

# View logs
tail -f /tmp/warp-backend.log
tail -f /tmp/warp-frontend.log

# Git status
cd "/Users/mac_m3/Projects/WARP Ecosystem/atlas" && git status
cd "/Users/mac_m3/Projects/WARP Ecosystem/console" && git status
```

---

**Questions or Issues?** Refer to project-specific documentation:
- Backend: `/Users/mac_m3/Projects/WARP Ecosystem/atlas/README.md`
- Frontend: `/Users/mac_m3/Projects/WARP Ecosystem/console/WARP.md`
