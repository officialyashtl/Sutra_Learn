# SUTRA LEARN — AI REPOSITORY FORENSIC AUDIT
**Document Reference:** `docs/ai/00-repository-forensic-audit.md`  
**Classification:** Baseline Architectural Audit & Forensic Inspection  
**Specification Baseline:** SUTRA LEARN — AI ASCENSION 1000  
**Audit Date:** November 1, 2026  
**Auditor:** Principal AI Systems Architect & Staff Full-Stack Engineer  

---

## 1. Executive Forensic Summary
This document records the exact state of the SUTRA LEARN repository prior to implementing the comprehensive Multi-Model AI Infrastructure (AI Ascension 1000).

The platform currently operates as an adaptive mathematics learning platform for NCERT Class 8 Linear Equations in One Variable with a FastAPI backend, React/Vite frontend, and SQLite database. Prior iterations established baseline AI endpoints, student chat flows, educator analytics, and an initial abstraction in `backend/app/ai/provider.py`.

However, the previous AI implementation lacked:
1. Typed, validated, centralized configuration management (`pydantic-settings`).
2. An official Google GenAI SDK client supporting dynamic model discovery and granular failure classification.
3. Decoupled Ollama adapters for `qwen3.5:4b` and `gemma4:e2b` with proper token and thinking-process handling.
4. A formal Provider Registry and explicit 12-state Orchestration State Machine with unique Request IDs.
5. Provider-specific Circuit Breakers, exponential backoff, and retry jitter.
6. Mathematical transformation step validation for AI-generated outputs.
7. Dedicated diagnostic and verification scripts in `scripts/ai/`.

---

## 2. Actual Repository Structure (AI Subsystem)

```
c:\Users\Yash\OneDrive\Desktop\Sutra_Learn\
├── backend/
│   ├── app/
│   │   ├── ai/
│   │   │   ├── __init__.py
│   │   │   ├── curriculum_context.py       # Retrieves curriculum & student context
│   │   │   └── provider.py                 # Monolithic provider abstraction
│   │   ├── auth/                           # JWT & PBKDF2 authentication
│   │   ├── content/                        # NCERT concept graph & questions
│   │   ├── db/
│   │   │   ├── database.py                 # SQLite WAL connection
│   │   │   └── crud.py                     # ai_conversations, ai_messages
│   │   ├── engine/                         # Deterministic adaptive engine
│   │   ├── routers/
│   │   │   ├── educator_assistant.py       # POST /api/v1/teacher/assistant/analyze
│   │   │   ├── tutor.py                    # POST /api/v1/tutor/chat
│   │   │   └── ...
│   │   └── main.py                         # GET /api/v1/ai/health
│   └── tests/
│       ├── test_ai.py                      # Tutor chat, grounding, teaching modes
│       └── ...
├── frontend/
│   └── src/
│       ├── pages/
│       │   ├── StudentTutor.tsx            # Student AI chat interface
│       │   ├── EducatorAssistant.tsx       # Teacher classroom AI intelligence
│       │   └── ...
│       └── services/api.ts
├── scripts/
│   ├── verify_e2e.py                       # 14-stage E2E suite
│   ├── verify_frontend_interactions.py     # 19-stage browser interaction suite
│   └── verify_mathematics.py               # Algebraic proof test suite
└── docs/                                   # System architecture records
```

---

## 3. Existing Provider Implementation & Behavior

### 3.1 `backend/app/ai/provider.py`
- Defined abstract base class `BaseAIProvider` with two methods:
  - `generate_tutor_response(...)`
  - `generate_educator_insight(...)`
- Implemented `CurriculumGroundedFallbackProvider`: Deterministic pedagogical rule-based generator anchored to NCERT Class 8 curriculum concepts.
- Implemented legacy `GeminiProvider`: Used raw `httpx` to call the legacy Google Gemini endpoint with basic dictionary parsing.
- Implemented preliminary `OllamaProvider`: Bundled model checking and generation into a single class without model-specific token controls or thinking-stream management.
- Implemented factory function `get_ai_provider()`: Evaluated `AI_PROVIDER` environment variable with basic if-else logic.

### 3.2 Live Environment & Model Inventory Findings
Forensic live probes conducted on the local machine revealed:
- **Ollama Runtime:** Active on `http://127.0.0.1:11434`.
- **Installed Models:**
  - `qwen3.5:4b` (ID: `d8b0f5e9760c`, 3.3 GB). Note: As a reasoning model, it produces an internal `thinking` stream which must be properly bounded or parsed so as not to exhaust timeouts on CPU inference.
  - `gemma4:e2b` (ID: `b37049369adf`, 4.6 GB). Generates standard assistant content with sub-300ms evaluation latency on warm cache.
- **Google Gemini API:**
  - Official SDK `google-genai` (v2.34.0) installed.
  - Provided API key authenticated successfully against `client.models.list()`, exposing 60 models.
  - Models `gemini-2.5-flash` returned 404 (deprecated for new projects, redirecting to `gemini-3.8-flash`).
  - Generation calls returned HTTP 403 `PERMISSION_DENIED` ("The Gemini API free tier is not available for this project. To use the Gemini API, please set up billing...").
  - This real-world condition mandates precise classification as `PERMISSION_DENIED`, marking Gemini as `UNAVAILABLE`, and cleanly activating local Ollama failover.

---

## 4. Existing Database Entities (`ai_conversations`, `ai_messages`)

Located in `backend/app/db/database.py` and `backend/app/db/crud.py`:
- **`ai_conversations` Table:**
  - `id` (TEXT PRIMARY KEY)
  - `owner_id` (TEXT, foreign key to users/learners)
  - `owner_role` (TEXT: 'student' | 'teacher')
  - `conversation_type` (TEXT: 'tutor' | 'educator_assistant')
  - `title` (TEXT)
  - `concept_id` (TEXT, optional)
  - `created_at` (TIMESTAMP)
  - `updated_at` (TIMESTAMP)
- **`ai_messages` Table:**
  - `id` (TEXT PRIMARY KEY)
  - `conversation_id` (TEXT, foreign key)
  - `sender_role` (TEXT: 'user' | 'assistant' | 'system')
  - `content` (TEXT)
  - `response_type` (TEXT: 'question', 'guided_explanation', 'worked_example', etc.)
  - `hints_json` (TEXT)
  - `concept_id` (TEXT)
  - `requires_follow_up` (INTEGER 0/1)
  - `provider_metadata` (TEXT JSON: records provider, model, is_fallback, fallback_reason)
  - `created_at` (TIMESTAMP)

*Assessment:* The existing database schema is sound, supports arbitrary JSON in `provider_metadata`, enforces foreign keys, and will be preserved 100% without breaking changes.

---

## 5. Identified Defects & Architectural Gaps

1. **Configuration Fragmentation:** Configuration parameters were read via direct `os.environ.get()` calls scattered across files rather than a centralized, validated `pydantic-settings` model.
2. **Missing Provider Registry:** No structured registry tracking live health, latency percentiles, error classification, circuit breaker state, or legal state transitions.
3. **No Explicit Request Lifecycle State Machine:** Request execution lacked traceable Request IDs and discrete state tracking (`RECEIVED` $\rightarrow$ `COMPLETED`).
4. **No Mathematical Step Validation:** AI-generated algebraic steps were returned without deterministic verification against algebraic transformation laws.
5. **Circuit Breakers Missing:** Repeated failures against unavailable endpoints (such as cloud API quota or unstarted local models) lacked automated circuit tripping and cooldown probes.
6. **No Windows AI Diagnostic Scripts:** Missing automated PowerShell scripts in `scripts/ai/` to verify local environments independently.

---

## 6. Target Architecture & Modification Plan

To reach 1,000 / 1,000 points without breaking existing workflows:
1. **`backend/app/ai/config.py`**: Implement centralized Pydantic settings with full typing, defaults, and validation rules.
2. **`backend/app/ai/models.py`**: Define schemas for Provider Registry, Health, Request State, and Telemetry.
3. **`backend/app/ai/gemini_adapter.py`**: Official `google.genai` SDK adapter with exact error classification (403, 404, 429, timeouts).
4. **`backend/app/ai/ollama_adapters.py`**: Separate `QwenAdapter` (`qwen3.5:4b`) and `GemmaAdapter` (`gemma4:e2b`) with token and thinking controls.
5. **`backend/app/ai/registry.py`**: Central provider registry managing states (`AVAILABLE`, `UNAVAILABLE`, `DEGRADED`, `CIRCUIT_OPEN`).
6. **`backend/app/ai/circuit_breaker.py`**: Provider-specific circuit breakers with exponential backoff and half-open probes.
7. **`backend/app/ai/math_validator.py`**: Deterministic equation transformation validator.
8. **`backend/app/ai/orchestrator.py`**: 12-state request orchestrator with traceable Request IDs.
9. **`backend/app/ai/provider.py`**: Refactor to route requests through the orchestrator while preserving existing public method contracts.
10. **`backend/app/routers/ai.py`**: Expose dedicated health, provider diagnostics, and execution endpoints.
11. **`scripts/ai/*.ps1`**: Create complete suite of Windows diagnostic scripts.
12. **`docs/ai/*.md`**: Create all 21 mandated architecture, provider, security, and verification documents.

