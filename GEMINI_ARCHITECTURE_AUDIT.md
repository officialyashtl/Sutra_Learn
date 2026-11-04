# SUTRA LEARN — GEMINI ARCHITECTURE AUDIT
## END-TO-END FLOW, COMPONENT BOUNDARIES & LIFECYCLE TOPOLOGY

**Project:** SUTRA LEARN  
**Evaluation Standard:** Gemini Omega 10,000 Architecture Specification  
**Timestamp:** November 4, 2026 (22:20 IST / 16:50 UTC)  
**Author:** Yash TL  
**Architecture Status:** **VERIFIED & OPERATIONAL**  

---

## 1. COMPREHENSIVE ARCHITECTURE MAP

```
[ BROWSER / CLIENT ]
       │
       ▼  (React 18 / TypeScript SPA: frontend/src/pages/StudentTutor.tsx)
[ HTTP CLIENT & JWT AUTH ]
       │  POST /api/v1/tutor/chat  (Headers: Authorization: Bearer <jwt>, Content-Type: application/json)
       ▼
[ FASTAPI APPLICATION BACKEND ]  (backend/app/main.py)
       │  ├─ APITraceMiddleware: assigns correlation_id, measures duration, logs API_TRACE
       │  ├─ CORSMiddleware: allows https://sutralearn.vercel.app, handles OPTIONS preflight
       │  └─ ai_rate_limiter: enforces sliding-window limit (20 req/min per student)
       ▼
[ TUTOR SERVICE ROUTER ]  (backend/app/routers/tutor.py)
       │  ├─ Verify JWT via get_current_user(Depends(get_current_user))
       │  ├─ Enforce conversation ownership (reject cross-student access with HTTP 403)
       │  ├─ Persist student's incoming inquiry into `ai_messages` (role: 'user')
       │  ├─ Retrieve bounded conversation history (last 6 messages)
       │  └─ Extract curriculum grounding context for concept (e.g. MATH-C01)
       ▼
[ MULTI-MODEL AI ORCHESTRATOR ]  (backend/app/ai/orchestrator.py)
       │  ├─ State: RECEIVED ─► VALIDATING ─► AUTHORIZING ─► BUILDING_CONTEXT
       │  ├─ State: SELECTING_PROVIDER via AIProviderRegistry (backend/app/ai/registry.py)
       │  └─ Evaluate Provider Health & Circuit Breaker status for 'gemini'
       ▼
[ GEMINI ADAPTER ]  (backend/app/ai/gemini_adapter.py)
       │  ├─ Official Google GenAI SDK: `from google import genai; from google.genai import types`
       │  ├─ Instantiation: genai.Client(api_key=..., http_options=types.HttpOptions(timeout=60000))
       │  ├─ Injects NCERT Class 8 Pedagogical Guidelines & Balance Principle into System Instruction
       │  └─ Resilient Cascade Loop: Primary `gemini-flash-lite-latest`
       ▼
[ GOOGLE CLOUD GEMINI REST / GRPC API ]  (generativelanguage.googleapis.com)
       │  ├─ HTTPS TLS 1.3 Handshake & API Key Authentication
       │  └─ Asynchronous Content Generation (client.aio.models.generate_content)
       ▼
[ RESPONSE VALIDATION & OBSERVABILITY ]
       │  ├─ Extract Candidate Text & Token Usage Metadata
       │  ├─ MathematicalValidator.validate_step_consistency: proves algebraic step validity
       │  └─ Record Circuit Breaker success / failure
       ▼
[ PERSISTENCE & AUDIT SERVICE ]  (backend/app/services/audit.py & backend/app/db/crud.py)
       │  ├─ Persist assistant reply to `ai_messages` (role: 'assistant', provider_metadata)
       │  ├─ Update `ai_conversations` updated_at timestamp
       │  └─ Append structured immutable record to `system_audit_logs` (correlation_id, full metadata)
       ▼
[ BROWSER RENDERING ]
       │  HTTP 200 OK Response (JSON payload matching TutorChatResponse)
       ▼  Client state update, Markdown formatting, KaTeX equation display, and history reload
```

---

## 2. COMPONENT RESPONSIBILITY MATRIX

| Component | Physical Location | Primary Architectural Responsibility | Verification Status |
|---|---|---|---|
| **Client UI** | `frontend/src/pages/StudentTutor.tsx` | UI input, Socratic chat stream, hints, LaTeX math formatting, and error notifications | **VERIFIED** |
| **Auth Guard** | `backend/app/auth.py` | JWT verification, persona binding, role verification, and expiration detection | **VERIFIED** |
| **API Entrypoint** | `backend/app/main.py` | CORS header enforcement, correlation ID injection, request tracing middleware | **VERIFIED** |
| **Tutor Router** | `backend/app/routers/tutor.py` | Rate limiting, conversation ownership validation, request lifecycle dispatch, persistence | **VERIFIED** |
| **AI Orchestrator** | `backend/app/ai/orchestrator.py` | 12-state request lifecycle machine, provider selection, mathematical validation | **VERIFIED** |
| **Gemini Adapter** | `backend/app/ai/gemini_adapter.py` | Official `google-genai` SDK integration, timeout enforcement, exponential retry backoff | **VERIFIED** |
| **External API** | `generativelanguage.googleapis.com` | Live Google Cloud Gemini API inference server | **VERIFIED** |
| **Math Validator** | `backend/app/ai/math_validator.py` | Proves balance operation consistency, detects algebraic hallucinations | **VERIFIED** |
| **Audit Service** | `backend/app/services/audit.py` | Immutable append-only audit trail logging with secret sanitization | **VERIFIED** |
| **Database Layer** | `backend/app/db/database.py` | Persistent SQLite storage (`sutra-data` /var/data on Render, WAL mode) | **VERIFIED** |

---

## 3. LIFECYCLE EVENT TRACEABILITY

Every request flowing through SUTRA LEARN emits structured lifecycle events tagged with a single unified `correlation_id`:

1. `REQUEST_RECEIVED`: Incoming HTTP POST request captured at router boundary.
2. `AUTHENTICATION_VERIFIED`: JWT token verified against `SUTRA_SECRET_KEY`.
3. `TUTOR_REQUEST_VALIDATED`: Concept ID and input lengths verified.
4. `GEMINI_CLIENT_READY`: `genai.Client` verified with non-empty credentials and configured timeout.
5. `GEMINI_REQUEST_STARTED`: Invocations dispatched via `client.aio.models.generate_content`.
6. `GEMINI_RESPONSE_RECEIVED`: Raw text, token count, and latency captured.
7. `GEMINI_RESPONSE_VALIDATED`: Algebraic consistency confirmed via `MathematicalValidator`.
8. `CONVERSATION_PERSISTED`: Message committed to SQLite `ai_messages` table.
9. `RESPONSE_DELIVERED`: Full JSON response transmitted to client with HTTP 200.

