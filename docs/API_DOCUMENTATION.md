# SUTRA LEARN — API DOCUMENTATION & CONTRACT SPECIFICATION
**Version:** 1.0.0 (Production Release)  
**Base URL:** `https://sutra-learn-api.onrender.com` (Production) / `http://127.0.0.1:8000` (Local)  
**Protocol:** HTTPS / JSON REST  
**Security:** Bearer Token (HMAC-SHA256) & Correlation Tracing (`X-Correlation-ID`)  

---

## 1. Authentication & Session Endpoints (`/api/v1/auth`)

### `POST /api/v1/auth/login`
Authenticates a student or teacher using their unique username/identifier and password.
- **Request Body:**
  ```json
  {
    "identifier": "student-01",
    "password": "password123"
  }
  ```
- **Success Response (`200 OK`):**
  ```json
  {
    "access_token": "sutra.eyJzdWIiOiJzdHVkZW50LTAxIiwicm9sZSI6InN0dWRlbnQiLCJuYW1lIjoiQWFyYXYgU2hhcm1hIiwiaWF0IjoxNzYyMzUzNjAwLCJleHAiOjE3NjI0NDAwMDB9.SIGNATURE",
    "token_type": "Bearer",
    "user": {
      "id": "student-01",
      "name": "Aarav Sharma",
      "grade": 8,
      "role": "student"
    }
  }
  ```
- **Error Responses:** `401 Unauthorized` (Invalid credentials), `422 Validation Error`.

### `POST /api/v1/auth/session`
Issues an authenticated session token for a pre-seeded learner persona (useful for rapid student onboarding and testing).
- **Request Body:**
  ```json
  {
    "learner_id": "student-01"
  }
  ```
- **Success Response (`200 OK`):**
  ```json
  {
    "access_token": "sutra.eyJzdWIiOi...",
    "token_type": "Bearer",
    "user_id": "student-01",
    "name": "Aarav Sharma",
    "role": "student"
  }
  ```
- **Error Responses:** `404 Not Found` (Learner does not exist).

### `GET /api/v1/auth/me`
Returns the identity and role profile of the currently authenticated Bearer token.
- **Headers:** `Authorization: Bearer <token>`
- **Success Response (`200 OK`):**
  ```json
  {
    "id": "student-01",
    "name": "Aarav Sharma",
    "grade": 8,
    "role": "student"
  }
  ```

---

## 2. Curriculum & Learning Graph Endpoints (`/api/v1/concepts`)

### `GET /api/v1/concepts`
Returns the complete NCERT Class 8 Mathematics concept registry (30 concepts) along with the prerequisite dependency graph. If an `Authorization: Bearer <token>` header is supplied, `is_unlocked` and `missing_prerequisites` are computed dynamically based on the learner's mastery records.
- **Headers:** `Authorization: Bearer <token>` (Optional)
- **Success Response (`200 OK`):**
  ```json
  {
    "concepts": [
      {
        "id": "MATH-C01",
        "code": "INT_ARITH",
        "title": "Integer Arithmetic",
        "grade": 8,
        "subject": "Mathematics",
        "description": "Rules of signs, additive inverses, and negative numbers.",
        "prerequisites": [],
        "order_index": 1,
        "is_unlocked": true,
        "missing_prerequisites": []
      },
      {
        "id": "MATH-C02",
        "code": "EQ_BALANCE",
        "title": "Equality and The Balance Principle",
        "grade": 8,
        "subject": "Mathematics",
        "description": "Treating equations like scales; performing equal operations to both sides.",
        "prerequisites": ["MATH-C01"],
        "order_index": 2,
        "is_unlocked": false,
        "missing_prerequisites": ["MATH-C01"]
      }
    ],
    "prerequisite_graph": {
      "MATH-C01": [],
      "MATH-C02": ["MATH-C01"]
    }
  }
  ```

### `GET /api/v1/concepts/{concept_id}`
Returns granular pedagogical lesson content, learning objectives, worked step-by-step examples, common pitfalls, and interactive prompts.
- **Path Parameters:** `concept_id` (e.g., `MATH-C01`)
- **Success Response (`200 OK`):**
  ```json
  {
    "id": "MATH-C01",
    "code": "INT_ARITH",
    "title": "Integer Arithmetic",
    "lesson": {
      "concept_id": "MATH-C01",
      "title": "Mastering Integer Operations & Signs",
      "objective": "Understand and apply the rules for adding, subtracting, multiplying, and dividing integers.",
      "key_principles": [
        "Adding a negative number is equivalent to subtracting its absolute value.",
        "Subtracting a negative number is equivalent to adding its positive counterpart."
      ],
      "worked_steps": [
        {
          "step_number": 1,
          "action": "Identify double signs",
          "expression": "5 - (-3)",
          "reasoning": "Subtracting a negative yields addition: 5 + 3 = 8."
        }
      ],
      "common_pitfalls": [
        "Confusing subtraction of negatives with multiplying two negatives."
      ]
    }
  }
  ```

### `GET /api/v1/concepts/{concept_id}/questions`
Returns diagnostic multiple-choice items with distractor tags, difficulty ratings, hints, and cognitive demand classifications.
- **Path Parameters:** `concept_id` (e.g., `MATH-C01`)
- **Success Response (`200 OK`):** Array of question objects.

---

## 3. Assessment & Evaluation Endpoints (`/api/v1/assessments`, `/api/v1/attempts`)

### `POST /api/v1/attempts`
Idempotent submission of an individual question attempt. Updates the spaced-retrieval memory trace automatically.
- **Headers:** `Authorization: Bearer <token>`
- **Request Body:**
  ```json
  {
    "attempt_id": "att-7b89f81a-6379-4d37-8f55-1211b439501a",
    "learner_id": "student-01",
    "question_id": "Q-INT-001",
    "concept_id": "MATH-C01",
    "selected_option_id": "A",
    "hint_used": false,
    "session_id": "sess-9a08e1",
    "client_timestamp": "2026-11-05T20:00:00Z"
  }
  ```
- **Success Response (`200 OK`):**
  ```json
  {
    "attempt_id": "att-7b89f81a-6379-4d37-8f55-1211b439501a",
    "is_duplicate": false,
    "is_correct": true,
    "hint_used": false,
    "selected_option_id": "A",
    "correct_option_id": "A",
    "explanation": "Adding a negative is equivalent to subtracting: 7 + (-12) = 7 - 12 = -5.",
    "misconception_tag": "none",
    "message": "Attempt recorded successfully."
  }
  ```

### `POST /api/v1/assessments/complete`
Authoritative backend evaluation of an entire concept assessment. Calculates raw score, percentage, passing threshold, diagnoses misconceptions, invokes Gemini for Socratic guidance (with NCERT fallback), evaluates adaptive next-lesson progression, and persists the result.
- **Headers:** `Authorization: Bearer <token>`
- **Request Body:**
  ```json
  {
    "concept_id": "MATH-C01",
    "session_id": "sess-4a8f902",
    "submissions": [
      { "question_id": "Q-INT-001", "selected_option_id": "A", "hint_used": false },
      { "question_id": "Q-INT-002", "selected_option_id": "C", "hint_used": false },
      { "question_id": "Q-INT-003", "selected_option_id": "A", "hint_used": false },
      { "question_id": "Q-INT-004", "selected_option_id": "A", "hint_used": false },
      { "question_id": "Q-INT-005", "selected_option_id": "A", "hint_used": false }
    ]
  }
  ```
- **Success Response (`200 OK`):**
  ```json
  {
    "id": "res-91603826-b9f9-4bcf-baf7-76757263e546",
    "session_id": "sess-4a8f902",
    "learner_id": "student-01",
    "concept_id": "MATH-C01",
    "concept_title": "Integer Arithmetic",
    "score": 5,
    "total_questions": 5,
    "percentage": 100.0,
    "passed": true,
    "outcome": "STRETCH",
    "next_concept_id": "MATH-C02",
    "next_concept_title": "Equality and The Balance Principle",
    "can_advance": true,
    "weak_concepts": [],
    "misconceptions_detected": [],
    "questions_detail": [
      {
        "question_id": "Q-INT-001",
        "prompt": "Evaluate: 7 + (-12)",
        "difficulty": 1,
        "cognitive_demand": "procedural",
        "selected_option_id": "A",
        "selected_option_text": "-5",
        "correct_option_id": "A",
        "correct_option_text": "-5",
        "is_correct": true,
        "hint_used": false,
        "explanation": "When adding numbers of opposite signs, subtract the smaller absolute value from the larger and keep the sign of the larger.",
        "options": []
      }
    ],
    "ai_guidance": {
      "summary": "Fantastic job! You achieved a perfect score of 5/5 on Integer Arithmetic...",
      "strengths": ["Rigorous application of core principles", "Clear procedural accuracy without hints"],
      "focus_area": "Maintain this precision on more advanced, multi-step problems.",
      "action_step": "Advance directly to your next unlocked lesson on Equality and Balance.",
      "provider": "Google Gemini",
      "is_fallback": false
    },
    "created_at": "2026-11-05T20:00:00Z"
  }
  ```

### `GET /api/v1/assessments/results/{concept_id}`
Retrieves the latest completed assessment result for the authenticated learner on a given concept, allowing seamless restoration upon page refresh or re-login.
- **Headers:** `Authorization: Bearer <token>`
- **Success Response (`200 OK`):** `AssessmentResultResponse` object.
- **Error Responses:** `404 Not Found` (No prior completed assessment found).

---

## 4. Grounded AI Tutor Endpoints (`/api/v1/tutor`)

### `POST /api/v1/tutor/chat`
Conversational Socratic tutoring grounded in NCERT Class 8 Mathematics.
- **Headers:** `Authorization: Bearer <token>`
- **Request Body:**
  ```json
  {
    "message": "Why does multiplying two negative numbers give a positive number?",
    "concept_id": "MATH-C01",
    "mode": "guided",
    "conversation_id": "conv-1a2b3c"
  }
  ```
- **Success Response (`200 OK`):**
  ```json
  {
    "id": "msg-8f921a",
    "conversation_id": "conv-1a2b3c",
    "sender_role": "assistant",
    "content": "Think of multiplication on the number line: multiplying by a positive number moves in the same direction, while multiplying by a negative number reverses direction...",
    "response_type": "guided_explanation",
    "hints": [
      "Consider the pattern: 3 * (-2) = -6, 2 * (-2) = -4, 1 * (-2) = -2, 0 * (-2) = 0. What comes next?"
    ],
    "provider_metadata": {
      "provider": "Google Gemini",
      "model": "gemini-flash-lite-latest",
      "is_fallback": false
    }
  }
  ```

### `GET /api/v1/tutor/conversations`
Lists past conversation sessions belonging to the authenticated learner.
- **Headers:** `Authorization: Bearer <token>`
- **Success Response (`200 OK`):** Array of `AIConversation` objects.

### `DELETE /api/v1/tutor/conversations/{conv_id}`
Deletes a specific tutor conversation session and all its associated messages.
- **Headers:** `Authorization: Bearer <token>`
- **Success Response (`204 No Content`)**

---

## 5. Teacher & Cohort Endpoints (`/api/v1/teacher`)

All endpoints in this group strictly require a Bearer token with `role: "teacher"`. Any student token receives `403 Forbidden`.

### `GET /api/v1/teacher/cohort`
Returns cohort-wide performance metrics, student list, total attempts, accuracy percentages, and risk flags.

### `GET /api/v1/teacher/analytics/concepts`
Returns concept-level difficulty ratings, bottleneck indicators, and common recurring misconceptions across the classroom.

### `POST /api/v1/teacher/override`
Enables human educators to clinically override an automated adaptive decision with justification.
- **Request Body:**
  ```json
  {
    "learner_id": "student-01",
    "concept_id": "MATH-C01",
    "previous_outcome": "STRETCH",
    "overridden_outcome": "SCAFFOLD",
    "reason": "Teacher clinical observation: Student hesitated on mental negative addition during board work.",
    "teacher_id": "teacher-01"
  }
  ```
- **Success Response (`200 OK`):**
  ```json
  {
    "status": "success",
    "override_id": "ovr-48a01",
    "message": "Pedagogical override applied and logged to audit trail."
  }
  ```

### `GET /api/v1/teacher/audit`
Returns categorized system audit logs across security rejections, pedagogical interventions, and authorized actions.
