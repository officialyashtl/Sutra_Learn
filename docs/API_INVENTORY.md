# SUTRA LEARN — COMPLETE API INVENTORY & SERVICE CATALOG
**Document Version:** 1.0.0-OMEGA  
**Classification:** Core System Architecture & Forensic Audit  
**Author:** Yash TL (The Oath of Tyr)  
**System Base:** FastAPI 0.110+ • SQLite (WAL Mode) • React 18+ TypeScript  

---

## 1. Executive Summary & Inventory Topology

This catalog provides an exhaustive inventory of all 39 API endpoints available in the SUTRA LEARN backend (`backend/app/main.py`), their invocation pathways from the frontend client (`frontend/src/`), cryptographic security bounds, database touchpoints, and correlation-tracked audit events.

```
+----------------------------------------------------------------------------------------------------+
|                                      API ROUTE ARCHITECTURE                                        |
+----------------------------------------------------------------------------------------------------+
|  Base Path: /api/v1/                                                                               |
|  Security Middleware: APITraceMiddleware (X-Correlation-ID), Unified CORS, Rate Limit Stubs        |
|  Authentication Schemes: Bearer JWT (PBKDF2-HMAC-SHA256, 100k iters), Role RBAC (Student/Teacher) |
+----------------------------------------------------------------------------------------------------+
|  Subsystems:                                                                                       |
|  - System & Docs: /health, /api/v1, /docs, /redoc, /openapi.json                                    |
|  - Curriculum & Concepts: /api/v1/concepts/*                                                       |
|  - Assessment Engine: /api/v1/sessions/*, /api/v1/attempts, /api/v1/recommendations/*             |
|  - Learner Tracking: /api/v1/learners/* (Progress, Attempts, Metrics, Spaced Retrieval)            |
|  - Teacher & Pedagogy: /api/v1/teacher/* (Cohort, Overrides, Audit, Assistant)                     |
|  - Authentication: /api/v1/auth/* (Login, Session, Me, Logout)                                     |
|  - Socratic AI Tutor: /api/v1/tutor/* (Chat, Conversations, Deletion)                              |
|  - AI Orchestration & Diagnostics: /api/v1/ai/* (Providers, Health, Tutor, Educator)               |
+----------------------------------------------------------------------------------------------------+
```

---

## 2. Exhaustive Endpoint Specifications

### 2.1 System & Observability

#### 1. `GET /api/v1/health`
- **Operation ID:** `health_check` | **Router:** `main.py`
- **Auth Required:** None (Public)
- **Parameters:** None
- **Response (200 OK):**
  ```json
  {
    "status": "healthy",
    "service": "Sutra Learn Adaptive Engine",
    "version": "1.0.0",
    "timestamp": "2026-11-04T12:00:00Z"
  }
  ```
- **Frontend Caller:** Deployment health checks, SRE probe scripts, `LandingPage.tsx` runtime checker.
- **Database Operations:** Read-only ping to verify SQLite WAL connection.
- **Audit Event:** None (high-frequency ping exempt from audit bloat).

#### 2. `GET /api/v1`
- **Operation ID:** `api_info` | **Router:** `main.py`
- **Auth Required:** None (Public)
- **Response (200 OK):** Service metadata, documentation URLs, supported API versions.
- **Frontend Caller:** Service discovery.
- **Database Operations:** None.
- **Audit Event:** None.

---

### 2.2 Authentication & Identity Subsystem (`/api/v1/auth`)

#### 3. `POST /api/v1/auth/login`
- **Operation ID:** `login` | **Router:** `backend/app/routers/auth.py`
- **Auth Required:** None (Public)
- **Request Body (`LoginRequest`):**
  ```json
  {
    "username": "student-01",
    "password": "...",
    "role": "student"
  }
  ```
- **Response (200 OK):**
  ```json
  {
    "token": "sutra_jwt_eyJhbGciOi...",
    "user": {
      "id": "student-01",
      "name": "Aarav Sharma",
      "role": "student",
      "grade_level": 8
    }
  }
  ```
- **Error Responses:** `401 Unauthorized` (Invalid credentials, inactive account), `422 Unprocessable Entity`.
- **Frontend Caller:** `frontend/src/pages/LoginPage.tsx` (`handleSubmit`).
- **Database Operations:** `SELECT FROM learners` or `SELECT FROM teachers`; password hash validation.
- **Audit Event:** `SUCCESSFUL_AUTHORIZED_ACTIONS` (Category: `AUTHENTICATION_SUCCESS`) or `REJECTED_SECURITY_EVENTS` (Category: `AUTHENTICATION_FAILURE`).

#### 4. `POST /api/v1/auth/session`
- **Operation ID:** `create_session` | **Router:** `backend/app/routers/auth.py`
- **Auth Required:** None (Demo session initializer for quick evaluations)
- **Request Body:** `{"user_id": "student-01", "role": "student"}`
- **Response (200 OK):** Token and user payload without full password challenge.
- **Frontend Caller:** Demo modal, automated test harnesses.
- **Audit Event:** `SUCCESSFUL_AUTHORIZED_ACTIONS` (`SESSION_CREATION`).

#### 5. `GET /api/v1/auth/me`
- **Operation ID:** `get_me` | **Router:** `backend/app/routers/auth.py`
- **Auth Required:** Bearer JWT (`get_current_user`)
- **Headers:** `Authorization: Bearer <token>`
- **Response (200 OK):** Sanitized user profile (`id`, `name`, `role`, `grade_level`).
- **Error Responses:** `401 Unauthorized` (Expired or tampered token).
- **Frontend Caller:** `frontend/src/App.tsx` on page load to re-hydrate session.
- **Database Operations:** `SELECT FROM learners` / `teachers` by `user_id`.
- **Audit Event:** None.

#### 6. `POST /api/v1/auth/logout`
- **Operation ID:** `logout` | **Router:** `backend/app/routers/auth.py`
- **Auth Required:** Bearer JWT
- **Response (200 OK):** `{"status": "logged_out", "message": "Session invalidated"}`
- **Frontend Caller:** `frontend/src/components/common/Header.tsx`, `frontend/src/api/client.ts`.
- **Database Operations:** None (Stateless token discard + audit emission).
- **Audit Event:** `SUCCESSFUL_AUTHORIZED_ACTIONS` (`USER_LOGOUT`).

---

### 2.3 Curriculum Subsystem (`/api/v1/concepts`)

#### 7. `GET /api/v1/concepts`
- **Operation ID:** `list_concepts` | **Router:** `backend/app/routers/curriculum.py`
- **Auth Required:** None (Public read)
- **Parameters:** `grade: Optional[int]`, `chapter: Optional[str]`
- **Response (200 OK):** Array of concept models (`id`, `name`, `chapter`, `difficulty`, `prerequisites`, `bkt_params`).
- **Frontend Caller:** `App.tsx`, `LandingPage.tsx`, `CurriculumGrid.tsx`, `ConceptViewer.tsx`.
- **Database Operations:** `SELECT FROM concepts ORDER BY sequence_order`.
- **Audit Event:** None.

#### 8. `GET /api/v1/concepts/{concept_id}`
- **Operation ID:** `read_concept` | **Router:** `backend/app/routers/curriculum.py`
- **Auth Required:** None (Public read)
- **Path Parameters:** `concept_id: str` (e.g. `MATH-C01`)
- **Response (200 OK):** Full concept detail including instructional theory, prerequisite graph, learning objectives.
- **Error Responses:** `404 Not Found`.
- **Frontend Caller:** `StudentWorkspace.tsx`, `ConceptDetailModal.tsx`.
- **Database Operations:** `SELECT FROM concepts WHERE id = ?`.

#### 9. `GET /api/v1/concepts/{concept_id}/questions`
- **Operation ID:** `list_concept_questions` | **Router:** `backend/app/routers/curriculum.py`
- **Auth Required:** None (Practice bank access)
- **Path Parameters:** `concept_id: str`
- **Query Parameters:** `difficulty: Optional[int]`, `limit: int = 10`
- **Response (200 OK):** Array of question objects with options, latex explanations, and misconception tags.
- **Frontend Caller:** `InteractivePractice.tsx`, `AssessmentSession.tsx`.
- **Database Operations:** `SELECT FROM questions WHERE concept_id = ?`.

---

### 2.4 Assessment & Adaptive Engine (`/api/v1/attempts`, `/api/v1/recommendations`)

#### 10. `POST /api/v1/sessions/start`
- **Operation ID:** `start_assessment_session` | **Router:** `backend/app/routers/assessment.py`
- **Auth Required:** Optional Bearer (Associates learner when present)
- **Request Body:** `{"concept_id": "MATH-C01", "mode": "diagnostic"}`
- **Response (200 OK):** `session_id`, initial question pool, time limits.
- **Database Operations:** `INSERT INTO assessment_sessions`.
- **Audit Event:** `PEDAGOGICAL_INTERVENTIONS` (`SESSION_INITIALIZED`).

#### 11. `POST /api/v1/attempts`
- **Operation ID:** `submit_attempt` | **Router:** `backend/app/routers/assessment.py`
- **Auth Required:** Bearer JWT (Learner)
- **Request Body (`AttemptSubmission`):**
  ```json
  {
    "learner_id": "student-01",
    "question_id": "Q-LIN-001",
    "selected_answer": "B",
    "time_taken_seconds": 45,
    "hint_used": false
  }
  ```
- **Response (200 OK):**
  ```json
  {
    "is_correct": true,
    "detected_misconceptions": [],
    "step_validations": [],
    "bkt_updated_mastery": 0.864,
    "next_recommendation": {
      "action": "STRETCH",
      "concept_id": "MATH-C01",
      "rationale": "High independent accuracy demonstrated."
    }
  }
  ```
- **Error Responses:** `400 Bad Request`, `401 Unauthorized`, `404 Question Not Found`.
- **Frontend Caller:** `StudentWorkspace.tsx` (`handleAnswerSubmit`).
- **Database Operations:**
  - `SELECT FROM questions`
  - `INSERT INTO question_attempts`
  - `UPDATE learner_concept_mastery`
  - `INSERT INTO system_audit_logs` (Correlation tracking)
- **Audit Event:** `PEDAGOGICAL_INTERVENTIONS` (`ASSESSMENT_ATTEMPT_SUBMITTED`).

#### 12. `POST /api/v1/recommendations/evaluate`
- **Operation ID:** `evaluate_concept_progress` | **Router:** `backend/app/routers/assessment.py`
- **Auth Required:** Bearer JWT (Learner or Teacher)
- **Request Body:** `{"learner_id": "student-01", "concept_id": "MATH-C01"}`
- **Response (200 OK):** Deterministic adaptive engine decision (`CONFIRM`, `STRETCH`, `SCAFFOLD`, `BRIDGE_BACK`, `TEACHER_REVIEW`).
- **Frontend Caller:** `StudentWorkspace.tsx`, `TeacherDashboard.tsx`.
- **Database Operations:** Reads recent attempts from `question_attempts`.
- **Audit Event:** `PEDAGOGICAL_INTERVENTIONS` (`ADAPTIVE_ENGINE_EVALUATION`).

---

### 2.5 Learner Subsystem (`/api/v1/learners`)

#### 13. `GET /api/v1/learners`
- **Operation ID:** `list_learners` | **Router:** `backend/app/routers/learners.py`
- **Auth Required:** None / Public demo listing
- **Response (200 OK):** Array of registered learners with basic profile information.
- **Frontend Caller:** `App.tsx` (Student switcher), `TeacherDashboard.tsx`.
- **Database Operations:** `SELECT FROM learners`.

#### 14. `GET /api/v1/learners/{learner_id}/progress`
- **Operation ID:** `get_progress` | **Router:** `backend/app/routers/learners.py`
- **Auth Required:** Bearer JWT (Self or Teacher)
- **Response (200 OK):** List of concept masteries, current streak, chapters completed, overall mastery %.
- **Frontend Caller:** `StudentDashboard.tsx`, `App.tsx`.
- **Database Operations:** `SELECT FROM learner_concept_mastery WHERE learner_id = ?`.

#### 15. `GET /api/v1/learners/{learner_id}/attempts`
- **Operation ID:** `get_learner_attempts` | **Router:** `backend/app/routers/learners.py`
- **Auth Required:** Bearer JWT
- **Query Parameters:** `limit: int = 50`, `concept_id: Optional[str]`
- **Response (200 OK):** Chronological log of student question attempts, scores, and timings.
- **Frontend Caller:** `StudentProgress.tsx`, `PastSessionsPanel.tsx`.
- **Database Operations:** `SELECT FROM question_attempts WHERE learner_id = ? ORDER BY created_at DESC`.

#### 16. `GET /api/v1/learners/{learner_id}/metrics`
- **Operation ID:** `get_learner_metrics_endpoint` | **Router:** `backend/app/routers/learners.py`
- **Auth Required:** Bearer JWT
- **Response (200 OK):** Aggregated learning metrics (accuracy, hints used, error patterns, time-on-task).
- **Frontend Caller:** `StudentInsights.tsx`.
- **Database Operations:** Computed metrics over `question_attempts` and `learner_concept_mastery`.

#### 17. `GET /api/v1/learners/{learner_id}/spaced-retrieval`
- **Operation ID:** `get_learner_spaced_retrieval` | **Router:** `backend/app/routers/learners.py`
- **Auth Required:** Bearer JWT
- **Response (200 OK):** Ebbinghaus decay analysis, memory retention predictions, due review items.
- **Frontend Caller:** `SpacedRetrievalPanel.tsx`, `StudentDashboard.tsx`.
- **Database Operations:** Analyzes timestamp deltas in `question_attempts`.

---

### 2.6 Teacher & Classroom Pedagogy Subsystem (`/api/v1/teacher`)

#### 18. `GET /api/v1/teacher/cohort`
- **Operation ID:** `get_cohort` | **Router:** `backend/app/routers/teacher.py`
- **Auth Required:** Bearer JWT (Teacher role)
- **Response (200 OK):** Full roster of learners, mastery levels, active flags, and struggle indicators.
- **Frontend Caller:** `TeacherDashboard.tsx`.
- **Database Operations:** Complex join of `learners`, `learner_concept_mastery`, and `teacher_overrides`.

#### 19. `GET /api/v1/teacher/analytics/concepts`
- **Operation ID:** `get_concept_analytics` | **Router:** `backend/app/routers/teacher.py`
- **Auth Required:** Bearer JWT (Teacher role)
- **Response (200 OK):** Concept-by-concept cohort failure rates, top misconceptions, average time spent.
- **Frontend Caller:** `TeacherAnalytics.tsx`.
- **Database Operations:** Aggregation query across all learner attempts.

#### 20. `GET /api/v1/teacher/overrides`
- **Operation ID:** `list_overrides` | **Router:** `backend/app/routers/teacher.py`
- **Auth Required:** Bearer JWT (Teacher role)
- **Response (200 OK):** Log of all pedagogical overrides applied by educators.
- **Frontend Caller:** `TeacherInterventions.tsx`.
- **Database Operations:** `SELECT FROM teacher_overrides ORDER BY created_at DESC`.

#### 21. `POST /api/v1/teacher/override`
- **Operation ID:** `apply_override` | **Router:** `backend/app/routers/teacher.py`
- **Auth Required:** Bearer JWT (Teacher role)
- **Request Body:**
  ```json
  {
    "teacher_id": "teacher-01",
    "learner_id": "student-01",
    "concept_id": "MATH-C01",
    "overridden_outcome": "BRIDGE_BACK",
    "reason": "Observed confusion during live classroom board work."
  }
  ```
- **Response (200 OK):** Override confirmation record.
- **Frontend Caller:** `InterventionModal.tsx`.
- **Database Operations:** `INSERT INTO teacher_overrides`.
- **Audit Event:** `PEDAGOGICAL_INTERVENTIONS` (`TEACHER_OVERRIDE_APPLIED`).

#### 22. `GET /api/v1/teacher/interventions/{override_id}/effectiveness`
- **Operation ID:** `get_intervention_outcome` | **Router:** `backend/app/routers/teacher.py`
- **Auth Required:** Bearer JWT (Teacher role)
- **Path Parameters:** `override_id: str`
- **Response (200 OK):** Pre- vs. post-intervention mastery delta, accuracy comparison, misconception resolution status.
- **Frontend Caller:** `InterventionEffectivenessCard.tsx`.
- **Database Operations:** Comparative analysis in `crud.get_intervention_effectiveness`.

#### 23. `GET /api/v1/teacher/audit`
- **Operation ID:** `list_categorized_audit` | **Router:** `backend/app/routers/teacher.py`
- **Auth Required:** Bearer JWT (Teacher role)
- **Query Parameters:** `category: Optional[str]`, `limit: int = 100`
- **Response (200 OK):** Chronological system audit logs with correlation IDs.
- **Frontend Caller:** `AuditLogViewer.tsx`.
- **Database Operations:** `SELECT FROM system_audit_logs ORDER BY created_at DESC`.

#### 24. `GET /api/v1/teacher/metrics`
- **Operation ID:** `get_teacher_cohort_metrics` | **Router:** `backend/app/routers/teacher.py`
- **Auth Required:** Bearer JWT (Teacher role)
- **Response (200 OK):** High-level KPI metrics (average mastery, at-risk count, active interventions).
- **Frontend Caller:** `TeacherDashboard.tsx`.

#### 25. `POST /api/v1/teacher/assistant/analyze`
- **Operation ID:** `analyze_classroom` | **Router:** `backend/app/routers/educator_assistant.py`
- **Auth Required:** Bearer JWT (Teacher role)
- **Request Body:** `{"cohort_id": "class-8a", "query": "Which students need intervention in linear equations?"}`
- **Response (200 OK):** AI synthesized pedagogical guidance grounded in NCERT curriculum and verified cohort data.
- **Frontend Caller:** `EducatorAIAssistant.tsx`.
- **Audit Event:** `PEDAGOGICAL_INTERVENTIONS` (`EDUCATOR_ASSISTANT_QUERY`).

#### 26. `GET /api/v1/teacher/assistant/insights`
- **Operation ID:** `get_quick_insights` | **Router:** `backend/app/routers/educator_assistant.py`
- **Auth Required:** Bearer JWT (Teacher role)
- **Response (200 OK):** Automated heuristic alert cards (stagnant learners, high misconception clusters).
- **Frontend Caller:** `TeacherDashboard.tsx`.

---

### 2.7 Socratic AI Tutor Subsystem (`/api/v1/tutor`)

#### 27. `POST /api/v1/tutor/chat`
- **Operation ID:** `tutor_chat` | **Router:** `backend/app/routers/tutor.py`
- **Auth Required:** Bearer JWT (Learner role)
- **Request Body (`TutorChatRequest`):**
  ```json
  {
    "message": "Why do we flip the sign when dividing by a negative number in an inequality?",
    "conversation_id": "conv_123456",
    "concept_id": "MATH-C01",
    "learner_id": "student-01"
  }
  ```
- **Response (200 OK):**
  ```json
  {
    "conversation_id": "conv_123456",
    "message_id": "msg_789101",
    "response": "Think about the numbers 2 and 5 on a number line. Which one is greater? Now multiply both by -1...",
    "hints": ["Consider position relative to 0", "Test with concrete numbers"],
    "response_type": "socratic_question",
    "provider_used": "google-gemini",
    "mathematical_validation": "PASSED"
  }
  ```
- **Error Responses:** `400 Bad Request`, `401 Unauthorized`, `500 Internal Error` (falls back to deterministic pedagogical template).
- **Frontend Caller:** `AITutorChat.tsx`.
- **Database Operations:**
  - Verify conversation ownership in `ai_conversations`
  - `INSERT INTO ai_messages` (Learner message)
  - `INSERT INTO ai_messages` (Tutor message)
  - `INSERT INTO system_audit_logs` (Correlation tracking)
- **Audit Event:** `PEDAGOGICAL_INTERVENTIONS` (`SOCRATIC_TUTOR_MESSAGE`).

#### 28. `GET /api/v1/tutor/conversations`
- **Operation ID:** `list_conversations` | **Router:** `backend/app/routers/tutor.py`
- **Auth Required:** Bearer JWT (Learner role)
- **Response (200 OK):** List of past Socratic dialogue sessions owned by the authenticated learner.
- **Frontend Caller:** `AITutorChat.tsx` (Past sessions sidebar).
- **Database Operations:** `SELECT FROM ai_conversations WHERE owner_id = ? ORDER BY updated_at DESC`.

#### 29. `GET /api/v1/tutor/conversations/{conversation_id}`
- **Operation ID:** `get_conversation_detail` | **Router:** `backend/app/routers/tutor.py`
- **Auth Required:** Bearer JWT (Learner role - strict ownership enforcement)
- **Path Parameters:** `conversation_id: str`
- **Response (200 OK):** Conversation metadata and complete chronological message history with hints.
- **Error Responses:** `401 Unauthorized`, `403 Forbidden` (Cross-student boundary protection), `404 Not Found`.
- **Frontend Caller:** `AITutorChat.tsx`.
- **Database Operations:** `SELECT FROM ai_conversations`, `SELECT FROM ai_messages`.

#### 30. `DELETE /api/v1/tutor/conversations/{conversation_id}`
- **Operation ID:** `delete_conversation` | **Router:** `backend/app/routers/tutor.py`
- **Auth Required:** Bearer JWT (Learner role - strict ownership enforcement)
- **Response (200 OK):** `{"deleted": true, "conversation_id": "..."}`
- **Error Responses:** `403 Forbidden` (When trying to delete another student's conversation), `404 Not Found`.
- **Frontend Caller:** `AITutorChat.tsx`.
- **Database Operations:** `DELETE FROM ai_conversations WHERE id = ? AND owner_id = ?`.
- **Audit Event:** `SUCCESSFUL_AUTHORIZED_ACTIONS` (`CONVERSATION_DELETED`).

---

### 2.8 Direct AI Orchestration & Generation (`/api/v1/ai`)

#### 31. `GET /api/v1/ai/health`
- **Operation ID:** `get_ai_health` | **Router:** `backend/app/routers/ai.py`
- **Auth Required:** None (Diagnostic probe)
- **Response (200 OK):** AI provider connectivity status, active model name, latency, rate limit quotas.
- **Frontend Caller:** Developer console, SRE probes.

#### 32. `GET /api/v1/ai/providers`
- **Operation ID:** `list_ai_providers` | **Router:** `backend/app/routers/ai.py`
- **Auth Required:** None
- **Response (200 OK):** Active providers (`google-gemini`, `sutra-local-validator`).

#### 33. `POST /api/v1/ai/tutor`
- **Operation ID:** `direct_tutor_orchestration` | **Router:** `backend/app/routers/ai.py`
- **Auth Required:** Bearer JWT
- **Request Body:** Direct orchestration payload with prompt, context, and mathematical boundary constraints.
- **Response (200 OK):** Orchestrated response with validation pass/fail metadata.

#### 34. `POST /api/v1/ai/educator`
- **Operation ID:** `direct_educator_orchestration` | **Router:** `backend/app/routers/ai.py`
- **Auth Required:** Bearer JWT (Teacher role)
- **Request Body:** Educator prompt with student performance context.

#### 35. `POST /api/v1/ai/generate-diagnostic-item`
- **Operation ID:** `generate_diagnostic_item` | **Router:** `backend/app/routers/ai.py`
- **Auth Required:** Bearer JWT (Teacher role)
- **Request Body:** `{"concept_id": "MATH-C01", "target_misconception": "sign_inversion"}`
- **Response (200 OK):** Generated question item verified by sympy engine with deliberate distractors matching misconception taxonomy.

---

### 2.9 Documentation & OpenAPI Specifications

#### 36. `GET /openapi.json`
- **Operation ID:** `openapi` | **Router:** FastAPI Core
- **Auth Required:** None (Public)
- **Description:** Full OpenAPI 3.1.0 schema specification for the entire API.

#### 37. `GET /docs`
- **Operation ID:** `swagger_ui_html` | **Router:** FastAPI Core
- **Description:** Interactive Swagger UI documentation.

#### 38. `GET /docs/oauth2-redirect`
- **Operation ID:** `swagger_ui_redirect` | **Router:** FastAPI Core
- **Description:** OAuth2 redirect handler for Swagger UI authentication.

#### 39. `GET /redoc`
- **Operation ID:** `redoc_html` | **Router:** FastAPI Core
- **Description:** ReDoc technical API documentation interface.

---

## 3. Route Security & Access Control Matrix

| Category | Endpoint Pattern | Public | Learner | Teacher | Admin / Audit |
|:---|:---|:---:|:---:|:---:|:---:|
| **System** | `GET /health`, `/api/v1` | **YES** | YES | YES | YES |
| **Curriculum** | `GET /api/v1/concepts*` | **YES** | YES | YES | YES |
| **Auth** | `POST /api/v1/auth/login`, `/session` | **YES** | YES | YES | YES |
| **Auth** | `GET /api/v1/auth/me`, `POST /logout` | NO | **YES** | **YES** | **YES** |
| **Assessment**| `POST /api/v1/attempts`, `/recommendations/*` | NO | **YES** | YES | YES |
| **Learners** | `GET /api/v1/learners/{id}/*` | NO | **YES (Self)** | **YES** | **YES** |
| **Teacher** | `GET/POST /api/v1/teacher/*` | NO | NO | **YES** | **YES** |
| **Tutor** | `POST/GET/DELETE /api/v1/tutor/*` | NO | **YES (Owner)**| NO | **YES** |
| **AI Orchestration** | `POST /api/v1/ai/*` | NO | YES | **YES** | **YES** |

---

## 4. Database Persistence & Audit Touchpoint Mapping

```
                                      [API Endpoints]
                                             |
            +--------------------------------+-------------------------------+
            |                                |                               |
      [Read Routes]                    [Write Routes]                 [Auth Routes]
            |                                |                               |
   SELECT concepts,                 INSERT question_attempts,        PBKDF2 Password
   learners, mastery                UPDATE learner_concept_mastery,  Hash Verification
            |                       INSERT teacher_overrides,                |
            |                       INSERT ai_conversations,                 |
            |                       INSERT ai_messages                       |
            |                                |                               |
            +--------------------------------+-------------------------------+
                                             |
                                [APITraceMiddleware]
                                             |
                                 Propagates X-Correlation-ID
                                             |
                             [system_audit_logs] (WAL Durability)
                             - REJECTED_SECURITY_EVENTS
                             - PEDAGOGICAL_INTERVENTIONS
                             - SUCCESSFUL_AUTHORIZED_ACTIONS
```

Every state change and security boundary crossing in SUTRA LEARN is deterministically logged with cryptographic nonces and durable foreign key constraints in SQLite WAL mode.

