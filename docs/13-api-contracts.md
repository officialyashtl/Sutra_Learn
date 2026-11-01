# SUTRA LEARN — Authoritative API Contract Specification
**Document ID:** `docs/13-api-contracts.md`  
**Execution Standard:** Principal Software Architect + Senior Backend Engineer  
**Timestamp:** 2026-11-01T17:30:00+05:30  
**Status:** IMPLEMENTED, VALIDATED & STABLE  

---

## 1. Authentication & Security Architecture

All protected endpoints require a cryptographically signed HMAC-SHA256 Bearer token passed in the `Authorization` header:
`Authorization: Bearer <token>`

Direct identity headers (`X-User-ID`, `X-Teacher-ID`) are strictly rejected.

---

## 2. Exhaustive API Endpoint Reference

### 2.1 Authentication Endpoints (`/api/v1/auth`)

#### `POST /api/v1/auth/login` (Unified Entry)
- **Description:** Authenticates with identifier (Student ID, Teacher ID, username) and password. Server-side role resolution directs user to their authorized portal.
- **Request Body:**
  ```json
  {
    "identifier": "student-01",
    "password": "sutra123"
  }
  ```
- **Response (200 OK):**
  ```json
  {
    "access_token": "ey...",
    "token_type": "Bearer",
    "user_id": "student-01",
    "name": "Aarav Sharma",
    "role": "student",
    "expires_in": 86400,
    "redirect_to": "/student/home",
    "user": {
      "id": "student-01",
      "name": "Aarav Sharma",
      "role": "student",
      "grade": 8
    }
  }
  ```

#### `POST /api/v1/auth/session`
- **Description:** Issues signed token for verified demo personas.
- **Request Body:** `{"learner_id": "teacher-01"}`
- **Response (200 OK):** TokenResponse with `redirect_to: "/teacher/dashboard"`.

#### `GET /api/v1/auth/me`
- **Description:** Returns validated claims extracted from Bearer token.
- **Headers:** `Authorization: Bearer <token>`
- **Response (200 OK):** `{"id": "student-01", "name": "Aarav Sharma", "role": "student"}`

---

### 2.2 Curriculum Endpoints (`/api/v1/concepts`)

#### `GET /api/v1/concepts`
- **Description:** Retrieves all 6 concepts in the NCERT Class 8 Mathematics DAG with prerequisite relationships and unlock status.
- **Response (200 OK):** `{"concepts": [...]}`

#### `GET /api/v1/concepts/{concept_id}`
- **Description:** Returns detailed lesson content, key principles, worked examples, and pitfalls for a concept.
- **Response (200 OK):** Concept object with embedded `Lesson`.

---

### 2.3 Assessment & Attempt Endpoints (`/api/v1/assessments` & `/api/v1/attempts`)

#### `POST /api/v1/attempts` (Idempotent Submission)
- **Description:** Records an assessment attempt. Evaluates correctness, diagnoses misconceptions, and prevents duplicate inflation.
- **Request Body:**
  ```json
  {
    "attempt_id": "uuid-v4",
    "learner_id": "student-01",
    "question_id": "Q-LIN-001",
    "concept_id": "MATH-C05",
    "selected_option_id": "A",
    "hint_used": false,
    "client_timestamp": "2026-11-01T10:00:00Z"
  }
  ```
- **Response (200 OK):**
  ```json
  {
    "attempt_id": "uuid-v4",
    "is_duplicate": false,
    "is_correct": true,
    "hint_used": false,
    "selected_option_id": "A",
    "correct_option_id": "A",
    "explanation": "To isolate 2x, subtract 5 from both sides...",
    "misconception_tag": "none",
    "message": "Attempt successfully recorded."
  }
  ```

---

### 2.4 Canonical Metrics Endpoints

#### `GET /api/v1/learners/{id}/metrics`
- **Description:** Single Source of Truth for all 56 student metrics across Curriculum, Accuracy, Attempts, Mastery, Misconceptions, Assistance, Efficiency, and Outcomes.
- **Headers:** `Authorization: Bearer <token>` (Enforces student ownership or teacher role)
- **Response (200 OK):** Complete `LearnerMetrics` payload.

#### `GET /api/v1/teacher/metrics`
- **Description:** Aggregated cohort analytics across enrolled students, at-risk alerts, bottlenecks, and intervention success rates.
- **Headers:** `Authorization: Bearer <token>` (Requires `teacher` role)
- **Response (200 OK):** Complete `CohortMetrics` payload.

---

### 2.5 Teacher Workspace & Interventions (`/api/v1/teacher`)

#### `GET /api/v1/teacher/cohort`
- **Description:** Roster of enrolled learners with attempts, accuracy, and review alerts.

#### `POST /api/v1/teacher/override`
- **Description:** Human-in-the-loop intervention. Applies pedagogical override with mandatory clinical rationale ($\ge 5$ chars).
- **Request Body:**
  ```json
  {
    "learner_id": "student-01",
    "concept_id": "MATH-C01",
    "previous_outcome": "TEACHER_REVIEW",
    "overridden_outcome": "BRIDGE_BACK",
    "reason": "Student exhibits sign confusion on negative integers; prescribe remedial lesson."
  }
  ```

#### `GET /api/v1/teacher/interventions/{override_id}/effectiveness`
- **Description:** Quantitative outcome evaluation comparing pre-intervention vs post-intervention accuracy, misconception resolution, and retention status.

#### `GET /api/v1/teacher/audit`
- **Description:** Categorized system compliance audit trail (`PEDAGOGICAL_INTERVENTIONS`, `REJECTED_SECURITY_EVENTS`, `SYSTEM_EVENTS`).

---

### 2.6 AI Tutor & Intelligence (`/api/v1/tutor` & `/api/v1/educator-assistant`)

#### `POST /api/v1/tutor/chat`
- **Description:** Contextual Socratic tutor across 6 teaching modes. Ownership protected.
- **Request Body:**
  ```json
  {
    "message": "Why do we perform the same operation on both sides?",
    "concept_id": "MATH-C02",
    "mode": "guided_learning"
  }
  ```
- **Response (200 OK):**
  ```json
  {
    "conversation_id": "uuid",
    "message_id": "uuid",
    "answer": "Think of an equation like a balanced scale...",
    "response_type": "guided_explanation",
    "hints": ["Review balance principles."],
    "concept_id": "MATH-C02",
    "requires_follow_up": true,
    "provider_metadata": {
      "provider": "Ollama",
      "model": "gemma4:e2b",
      "is_fallback": false
    }
  }
  ```

---

### 2.7 Observability & Health Endpoints

#### `GET /api/v1/health`
- **Description:** Service health and SQLite WAL journal mode status.

#### `GET /api/v1/ai/health`
- **Description:** Multi-model AI status, Ollama reachability, installed models, and fallback readiness.

