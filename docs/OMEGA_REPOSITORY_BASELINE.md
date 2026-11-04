# SUTRA LEARN — OMEGA ∞
## DOCUMENT 01: FORENSIC REPOSITORY BASELINE & DISCOVERY REPORT

**Project:** SUTRA LEARN  
**System Designation:** Adaptive Learning & Mathematical Socratic Platform (NCERT Class 8)  
**Standard:** OMEGA Production Engineering Standard  
**Date of Audit:** November 4, 2026  
**Auditor:** Principal Software Architect & Release Engineering Lead  

---

### 1. EXECUTIVE SUMMARY & REPOSITORY CONTEXT

SUTRA LEARN is an enterprise-grade, offline-first, adaptive educational platform designed specifically for NCERT Class 8 Mathematics. The platform combines deterministic mastery tracking (Bayesian Knowledge Tracing, Spaced Retrieval, Prerequisite Dependency Graphs) with multi-model AI tutoring and teacher orchestration.

This forensic baseline establishes the complete state of the repository prior to and during the OMEGA ∞ integration of the Google GenAI / Gemini Developer API key (`AQ.Ab8...fiVQ [REDACTED_FOR_SECURITY]`).

---

### 2. REPOSITORY TOPOLOGY & PHYSICAL DIRECTORY STRUCTURE

The repository is organized as a unified full-stack monorepo:

```
c:\Users\Yash\OneDrive\Desktop\Sutra_Learn\
├── .env                              # Root runtime environment configuration
├── backend/                          # FastAPI Python backend application
│   ├── .env                          # Backend-specific environment variables
│   ├── app/
│   │   ├── __init__.py
│   │   ├── auth.py                   # PBKDF2-HMAC-SHA256 & JWT authentication
│   │   ├── auth_rate_limit.py        # Sliding-window in-memory IP & user rate limiter
│   │   ├── main.py                   # FastAPI initialization, CORS, and route mounting
│   │   ├── schemas.py                # Pydantic v2 schemas for requests & responses
│   │   ├── ai/                       # AI intelligence subsystem
│   │   │   ├── circuit_breaker.py    # 3-state circuit breaker (Closed, Open, Half-Open)
│   │   │   ├── config.py             # AISettings via pydantic-settings
│   │   │   ├── curriculum_context.py # NCERT grounding context builder
│   │   │   ├── gemini_adapter.py     # Official google-genai SDK adapter & fallback cascade
│   │   │   ├── math_validator.py     # Deterministic SymPy & AST mathematical validator
│   │   │   ├── models.py             # AI domain models, enums, error categories
│   │   │   ├── ollama_adapters.py    # Local runtime adapters (Qwen 3.5 4B & Gemma 4 E2B)
│   │   │   ├── orchestrator.py       # Multi-Model failover coordinator
│   │   │   ├── provider.py           # Provider abstraction & deterministic fallback
│   │   │   └── registry.py           # Dynamic model capability discovery & registry
│   │   ├── content/                  # NCERT Class 8 Mathematics curriculum
│   │   │   ├── concepts.py           # 6 core concepts (MATH-C01 to MATH-C06)
│   │   │   ├── models.py             # Curriculum domain dataclasses
│   │   │   └── questions.py          # 24 calibrated questions across 4 tiers
│   │   ├── db/                       # Persistence subsystem
│   │   │   ├── crud.py               # Complete transactional CRUD operations
│   │   │   ├── database.py           # SQLite connection pool with WAL mode & busy timeout
│   │   │   └── sutra.db              # SQLite persistent database file
│   │   ├── engine/                   # Authoritative learning intelligence
│   │   │   ├── adaptive.py           # Evidence-based decision engine
│   │   │   ├── policy.py             # Pedagogical transition rules & thresholds
│   │   │   └── spaced_retrieval.py   # Modified Leitner & forgetting curve engine
│   │   ├── routers/                  # API endpoints
│   │   │   ├── ai.py                 # Multi-model AI status & direct prompts
│   │   │   ├── assessment.py         # Submissions, evaluations & diagnostic paths
│   │   │   ├── auth.py               # Login, register, profile, and session management
│   │   │   ├── curriculum.py         # Textbook chapters, concepts, and worked examples
│   │   │   ├── educator_assistant.py # Teacher AI classroom insights
│   │   │   ├── learners.py           # Student profiles, mastery state, and streak logs
│   │   │   ├── teacher.py            # Teacher analytics, cohort trends & intervention alerts
│   │   │   └── tutor.py              # Student Socratic AI Tutor & past sessions
│   │   └── services/
│   │       └── metrics.py            # Latency, token, and error telemetry collector
│   └── tests/                        # Pytest suite
│       ├── conftest.py               # Pytest environment fixtures
│       ├── test_ai.py                # AI tutor, roles, and conversation isolation tests
│       ├── test_api.py               # Auth, session, and role security tests
│       ├── test_content.py           # Curriculum integrity and graph DAG acyclicity
│       ├── test_educational_excellence.py # Pedagogical accuracy tests
│       ├── test_engine.py            # BKT mastery and adaptive rule tests
│       └── test_scenarios.py         # End-to-end student learning pathways
├── frontend/                         # Vite + React 18 + TypeScript SPA
│   ├── package.json                  # Dependencies (Lucide, Tailwind, React Router)
│   ├── tsconfig.json                 # Strict TypeScript configuration
│   ├── vite.config.ts                # Build bundler configuration
│   ├── src/
│   │   ├── App.tsx                   # Top-level routing, auth restoration, offline sync
│   │   ├── index.css                 # Earthbound Editorial styling and design tokens
│   │   ├── main.tsx                  # React entry point
│   │   ├── api/                      # Client HTTP abstractions
│   │   │   └── client.ts             # Auth injection, token storage, and error mapping
│   │   ├── components/               # UI components
│   │   │   ├── Header.tsx            # Sticky navigation bar with role switcher
│   │   │   ├── Footer.tsx            # Editorial footer with Yash TL signature
│   │   │   ├── PastSessionsModal.tsx # Past session history inspector
│   │   │   └── ...
│   │   └── pages/                    # Views
│   │       ├── LandingPage.tsx       # Premium BrandProof recreation
│   │       ├── StudentDashboard.tsx  # Practice, mastery overview, and Socratic tutor
│   │       └── TeacherDashboard.tsx  # Classroom alerts, cohort metrics, and educator AI
├── docs/                             # Engineering documentation & evidence reports
└── scripts/                          # Automation, audit, and verification scripts
```

---

### 3. BACKEND ARCHITECTURE & DATA FLOW

The backend uses FastAPI mounted at port `8000`.

#### A. Request Pipeline
1. **HTTP Ingestion**: Standard HTTP/1.1 or HTTP/2 requests with TLS termination at Render edge.
2. **CORS Handling**: `CORSMiddleware` configured to allow `https://sutralearn.vercel.app`, local dev servers (`localhost:5173`, `localhost:3000`), with full header support (`Authorization`, `Content-Type`).
3. **Rate Limiting**: `app.auth_rate_limit.ai_rate_limiter` monitors client identifiers using a sliding window:
   - Auth endpoints: 10 requests per minute per IP.
   - AI endpoints: 20 inference requests per minute per authenticated learner.
4. **Authentication Dependency**: `get_current_user` extracts and cryptographically verifies JWT tokens signed via HMAC-SHA256 (`HS256`).
5. **Database Transaction**: SQLite in WAL (`Write-Ahead Logging`) mode with `PRAGMA busy_timeout = 10000;` prevents concurrent database locking.
6. **Multi-Model AI Dispatch**: Decoupled `get_ai_provider()` routes queries based on runtime mode (`cloud`, `local`, `auto`, `deterministic`).

---

### 4. FRONTEND ARCHITECTURE & DESIGN FIDELITY

- **Framework**: React 18 with TypeScript 5.
- **Styling Architecture**: Tailwind CSS with custom Earthbound Editorial design tokens:
  - Deep Umber: `#291C0E`
  - Terracotta Bark: `#6E473B`
  - Ochre Sand: `#A78D78`
  - Soft Clay: `#BEB5A9`
  - Muted Parchment: `#E1D4C2`
  - Linen Ground: `#F8F5EF`
  - Warm Card: `#F2ECE3`
  - Pure Paper: `#FFFEFC`
- **Routing**: Client-side stateful routing supporting:
  - Public Landing Page (`/`) with live interactive product preview
  - Student Workspace (`/student`)
  - Teacher Workspace (`/teacher`)
  - Offline Mode with local storage attempt buffering
- **Signatures**: Developer signature `Designed & Developed by Yash TL` with `YT` monogram stamp preserved in all footers.

---

### 5. AI SUBSYSTEM DISCOVERY & ACTIVE PROVIDERS

Prior to OMEGA ∞, the AI subsystem consisted of:
1. **Google Gemini Adapter** (`backend/app/ai/gemini_adapter.py`):
   - Uses modern `google-genai` SDK (`genai.Client(api_key=...)`).
   - Configured model was previously set to `gemini-3.8-flash`.
   - Lacked automated fallbacks for demand spikes (HTTP 503) and retired preview identifiers (HTTP 404).
2. **Ollama Local Adapters** (`backend/app/ai/ollama_adapters.py`):
   - Qwen 2.5/3.5 4B and Gemma 4 E2B via local REST endpoint `http://localhost:11434`.
3. **Curriculum-Grounded Deterministic Engine** (`backend/app/ai/provider.py`):
   - Grounded in NCERT Class 8 Chapter 2 (Linear Equations in One Variable).
   - Solves equations step-by-step using balance rules.
   - Identifies common student misconceptions (transposition sign errors, partial balance operations).

---

### 6. IDENTIFIED DEFECTS & REMEDIATION PLAN

| Defect ID | Severity | Subsystem | Description | Status |
|---|---|---|---|---|
| DEF-01 | High | AI Adapter | Hardcoded model name triggered HTTP 404/503 during Google API rotation | Fixed (Dynamic cascade) |
| DEF-02 | Medium | API Key Config | Stale key ending in `...b5NmJljPA` in `.env` | Fixed (Updated to `...D8fiVQ`) |
| DEF-03 | High | Windows Sandbox | ProactorEventLoop `socketpair()` hung during sandboxed `asyncio.run` | Fixed (Environment isolation guard) |
| DEF-04 | Medium | SQLite Locking | Concurrency bursts caused occasional `database is locked` | Fixed (`PRAGMA busy_timeout = 10000`) |
| DEF-05 | Low | Telemetry | Missing model candidate tracking on multi-turn tutor sessions | Fixed (Structured provider metadata) |

---

### 7. BASELINE ARTIFACT SIGN-OFF

The repository baseline is formally established and verified. No uncommitted working files were destroyed or reverted. All existing tests compile and pass cleanly.

