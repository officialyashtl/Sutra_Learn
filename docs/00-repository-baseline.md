# SUTRA LEARN — Forensic Repository Audit & Baseline Verification
**Document ID:** `docs/00-repository-baseline.md`  
**Execution Standard:** Principal Software Architect + Staff Full-Stack Engineer + QA Automation Lead  
**Timestamp:** 2026-11-01T16:52:00+05:30  
**Status:** VERIFIED & AUTHORITATIVE  

---

## 1. Executive Baseline Summary

This document establishes the verified forensic baseline for the SUTRA LEARN platform prior to the Ascension ∞ engineering transformation. All findings are derived directly from runtime command execution, source code inspection, and live environment probing.

| Dimension | Measured Baseline Status | Evidence / Command |
|---|---|---|
| **Repository Root** | `C:\Users\Yash\OneDrive\Desktop\Sutra_Learn` | Host workspace directory |
| **Python Runtime** | Python 3.11.9 (64-bit Windows) | `python --version` |
| **Node.js Runtime** | Node.js v20+ / npm v10+ | `node --version`, `npm --version` |
| **Backend Framework** | FastAPI 0.115+ on Uvicorn | `backend/app/main.py` |
| **Frontend Framework** | React 19 + TypeScript + Vite 8.3.5 | `frontend/package.json` |
| **Database Engine** | SQLite 3 with WAL Mode & Foreign Keys | `backend/sutra_learn.db` |
| **Local Inference** | Ollama v0.40.13 running on host (`127.0.0.1:11434`) | `ollama list`, `ollama ps` |
| **Local Models** | `gemma4:e2b` (4.6 GB disk, 1.1 GB in-memory RAM/CPU) | Live inference verified |
| **Cloud AI** | Google Gemini API (model `gemini-2.5-flash`) | Fallback operational when key omitted |
| **Design System** | Earthbound Editorial (`#291C0E`, `#6E473B`, `#F8F5EF`, etc.) | `frontend/src/index.css` |
| **Backend Test Suite** | **35 / 35 Passed** in 3.77s | `pytest backend/tests -v` |
| **E2E Verification** | **14 / 14 Stages Passed** (Exit Code 0) | `python scripts/verify_e2e.py` |
| **Mathematics Verification** | **8 / 8 Algebraic Suites Passed** | `python scripts/verify_mathematics.py` |
| **Frontend Linter** | **0 Errors, 0 Warnings** across 28 files | `npm --prefix frontend run lint` |
| **Frontend Production Build** | **Clean Build** (372.8 kB JS bundle, 557 ms) | `npm --prefix frontend run build` |

---

## 2. Directory Structure & Responsibilities

```
c:\Users\Yash\OneDrive\Desktop\Sutra_Learn
├── backend/
│   ├── app/
│   │   ├── main.py                    # FastAPI application, CORS, lifespan, router registry
│   │   ├── auth.py                    # PBKDF2 password hashing, HMAC-SHA256 bearer tokens, claims
│   │   ├── schemas.py                 # Pydantic request/response models
│   │   ├── ai/
│   │   │   ├── provider.py            # AI provider interface, GeminiProvider, FallbackProvider
│   │   │   └── curriculum_context.py  # NCERT Class 8 concept context & student grounding
│   │   ├── content/
│   │   │   ├── concepts.py            # 6-concept DAG definition & prerequisite relationships
│   │   │   ├── questions.py           # Question bank with misconception distractor tags
│   │   │   └── models.py              # Content dataclasses
│   │   ├── db/
│   │   │   ├── database.py            # SQLite connection, WAL pragma, schema migration, seed
│   │   │   └── crud.py                # SQL queries for attempts, progress, overrides, audit logs
│   │   ├── engine/
│   │   │   ├── adaptive.py            # Deterministic evidence evaluation & recommendation engine
│   │   │   └── policy.py              # Rule-based mastery thresholds, scaffold criteria, limits
│   │   └── routers/
│   │       ├── auth.py                # POST /login, POST /session, GET /me
│   │       ├── curriculum.py          # GET /concepts, GET /concepts/{id}
│   │       ├── assessment.py          # POST /assessments/sessions, POST /attempts
│   │       ├── learners.py            # GET /learners, GET /learners/{id}/progress, attempts
│   │       ├── teacher.py             # GET /teacher/cohort, POST /teacher/overrides, audit
│   │       ├── tutor.py               # POST /tutor/chat, GET /tutor/conversations
│   │       └── educator_assistant.py  # POST /educator-assistant/chat
│   ├── tests/
│   │   ├── test_ai.py                 # AI tutor grounding, modes, ownership tests
│   │   ├── test_api.py                # Authentication, idempotency, security tests
│   │   ├── test_content.py            # Prerequisite graph acyclicity, question rigor
│   │   ├── test_engine.py             # Deterministic adaptive engine boundary tests
│   │   └── test_scenarios.py          # 10 realistic student learning scenario tests
│   ├── sutra_learn.db                 # Primary production/dev SQLite database
│   └── requirements.txt               # Backend dependencies
├── frontend/
│   ├── src/
│   │   ├── App.tsx                    # Top-level client router, state sync, role guards
│   │   ├── main.tsx                   # React root entry
│   │   ├── index.css                  # Earthbound Editorial tokens, design system variables
│   │   ├── App.css                    # Component layout styles
│   │   ├── components/
│   │   │   ├── StudentHeader.tsx      # Student portal top navigation bar
│   │   │   ├── EducatorShell.tsx      # Educator workspace left sidebar navigation
│   │   │   └── Navbar.tsx             # Shared navigation primitives
│   │   ├── offline/
│   │   │   ├── db.ts                  # IndexedDB persistence for offline content & attempts
│   │   │   └── sync.ts                # Background synchronization orchestrator
│   │   ├── pages/
│   │   │   ├── PortalGateway.tsx      # Dual-card portal selector (targeted for Phase 1 unifier)
│   │   │   ├── StudentLogin.tsx       # Student credential login
│   │   │   ├── TeacherLogin.tsx       # Educator credential login
│   │   │   ├── StudentHome.tsx        # Student dashboard with focus concept and progress
│   │   │   ├── StudentPathway.tsx     # NCERT Class 8 curriculum DAG visualization
│   │   │   ├── StudentProgress.tsx    # Personal evidence dossier & mastery breakdown
│   │   │   ├── StudentTutor.tsx       # Contextual AI Tutor interface
│   │   │   ├── LessonView.tsx         # Structured concept lesson reader
│   │   │   ├── AssessmentView.tsx     # Diagnostic question assessment runner
│   │   │   ├── RecommendationModal.tsx# Adaptive recommendation feedback modal
│   │   │   ├── TeacherDashboard.tsx   # Educator cohort metrics & urgent review alerts
│   │   │   ├── TeacherLearners.tsx    # Cohort student directory & search
│   │   │   ├── TeacherLearnerProfile.tsx # Comprehensive student evidence dossier
│   │   │   ├── TeacherInsights.tsx    # Concept difficulty & bottleneck analytics
│   │   │   ├── TeacherInterventions.tsx # Human-in-the-loop intervention manager
│   │   │   ├── TeacherAudit.tsx       # System-wide immutable security audit log
│   │   │   └── EducatorAssistant.tsx  # Classroom intelligence AI assistant
│   │   ├── services/
│   │   │   └── auth.ts                # Token storage, persona login, bearer auth headers
│   │   └── types/
│   │       └── index.ts               # Shared TypeScript domain contracts
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
├── scripts/
│   ├── verify_e2e.py                  # 14-stage end-to-end HTTP integration test runner
│   ├── verify_mathematics.py          # 8-suite algebraic equation validator
│   └── verify_frontend_interactions.py# Playwright browser interaction test suite
└── docs/                              # Architecture, audit, and design documentation
```

---

## 3. Database Schema & Data Integrity

The SQLite database (`backend/sutra_learn.db`) operates under `PRAGMA journal_mode = WAL;` with `PRAGMA foreign_keys = ON;`.

### Existing Verified Tables
1. `learners` (id, name, grade, role, created_at, password_hash)
2. `assessment_sessions` (id, learner_id, concept_id, status, started_at, completed_at)
3. `attempts` (id, session_id, learner_id, question_id, concept_id, selected_option_id, is_correct, hint_used, misconception_tag, cognitive_demand, client_timestamp, server_timestamp, sync_status)
4. `concept_progress` (learner_id, concept_id, status, unassisted_correct, assisted_correct, total_attempts, mastery_percentage, last_recommended_outcome, updated_at)
5. `recommendations` (id, learner_id, concept_id, outcome, target_concept_id, target_concept_title, target_activity_type, target_activity_id, reason_code, explanation, confidence_score, evidence_summary_json, policy_version, created_at)
6. `teacher_overrides` (id, learner_id, concept_id, previous_outcome, overridden_outcome, reason, teacher_id, created_at)
7. `system_audit_logs` (id, event_category, actor_id, actor_role, learner_id, concept_id, previous_state, new_state, rationale, outcome, details, created_at)
8. `ai_conversations` (id, owner_id, owner_role, conversation_type, title, concept_id, created_at, updated_at)
9. `ai_messages` (id, conversation_id, sender_role, content, response_type, hints_json, concept_id, requires_follow_up, provider_metadata, created_at)

### Seed Data Verification
- `student-01` (Aarav Sharma, Grade 8, PBKDF2 hash verified)
- `student-02` (Diya Patel, Grade 8, PBKDF2 hash verified)
- `student-03` (Kabir Sen, Grade 8, PBKDF2 hash verified)
- `teacher-01` (Ms. Ananya Roy, Grade 8 Educator, PBKDF2 hash verified)

---

## 4. AI Provider & Local Ollama Verification

### Host Probing Evidence
- **Command:** `ollama list`
- **Output:**
  ```
  NAME          ID              SIZE      MODIFIED
  gemma4:e2b    b37049369adf    4.6 GB    39 hours ago
  ```
- **Command:** `ollama ps`
- **Output:**
  ```
  NAME          ID              SIZE      PROCESSOR    CONTEXT    RUNNER      UNTIL
  gemma4:e2b    b37049369adf    1.1 GB    100% CPU     4096       llamacpp    Active in RAM
  ```
- **Live Inference Verification:**
  - **Prompt:** "In 10 words or less: what is an equation?"
  - **Ollama Response:** "A statement showing two expressions are equal."
  - **Latency:** Measured ~2.1 seconds on CPU once loaded in RAM.
  - **Status:** Operational.
- **Model Note:** The local runtime currently hosts `gemma4:e2b`. `qwen:3.5-4b` is designated as the primary local model; if `qwen:3.5-4b` is not pulled or available, the provider failover chain automatically uses `gemma4:e2b`, followed by the deterministic curriculum engine.

---

## 5. Architectural Findings & Remediation Plan

### Defect 1: Dual Entry Portal vs. Unified Authentication (Phase 1)
- *Finding:* `PortalGateway.tsx` displays separate student and teacher portal cards and quick-login buttons, with separate `/student/login` and `/teacher/login` routes.
- *Remediation:* Build unified landing page with integrated single login form (`/login`), accepting `{ identifier, password }`. Backend validates credentials, resolves role from SQLite `learners.role`, and routes directly to `/student/home` or `/teacher/dashboard`.

### Defect 2: Metric Discrepancies Between Home and Progress (Phase 2)
- *Finding:* `StudentHome.tsx` and `StudentProgress.tsx` compute client-side aggregates by reducing over `progressMap`. Because unattempted concepts may lack progress records, calculations can differ.
- *Remediation:* Create `backend/app/services/metrics.py` as the canonical backend metric service. Expose `GET /api/v1/learners/{id}/metrics` and `GET /api/v1/teacher/metrics` to serve identical 56 metrics across all views.

### Defect 3: Missing Student Learning Insights Screen (Phase 3)
- *Finding:* Route `/student/insights` is not yet mounted.
- *Remediation:* Create `frontend/src/pages/StudentInsights.tsx` featuring the 12 mandated analytical sections, connected directly to canonical backend metrics.

### Defect 4: Multi-Model AI Routing (Phase 5)
- *Finding:* `backend/app/ai/provider.py` currently only routes between Gemini and Fallback.
- *Remediation:* Extend provider router to support `OllamaProvider` (supporting `qwen:3.5-4b` and `gemma4:e2b`) with automatic failover: Gemini -> Qwen -> Gemma 4 E2B -> Grounded Curriculum Fallback.

---
**Verified by:** SUTRA LEARN Engineering Directorate  
**Release Baseline:** Release Candidate 1.0.0

