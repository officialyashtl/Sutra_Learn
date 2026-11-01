# SUTRA LEARN — Release Candidate Independent Acceptance Audit

**Document Version:** 1.0.0  
**Audit Date:** November 1, 2026  
**Auditor Role:** Lead Systems Auditor, Educational Technology Specialist & Principal Security Engineer  
**Audit Standard:** Zero-Assumptions Independent Verification  

---

## 1. Executive Summary & Audit Scope

This document represents an independent, adversarial audit of the SUTRA LEARN Release Candidate (RC 1.0.0). Every major technical claim made in previous execution reports was audited against the actual source code, SQLite schema, runtime processes, and browser automation drivers.

### Release Decision: **RELEASE CANDIDATE (RC 1.0.0 APPROVED FOR STAGING / CONTROLLED CLASSROOM PILOT)**

> **Summary Verdict**: The core functional, pedagogical, mathematical, security, and interface claims are **VERIFIED** through working code, reproducible automated tests, and live browser automation. However, critical discrepancies between academic claims in the previous report (such as theoretical Bayesian Knowledge Tracing formulas vs. the actual rule-based deterministic scoring engine) and production infrastructure gaps (lack of application-level rate limiting, unverified live cloud deployment) necessitate that this build is certified as **RELEASE CANDIDATE**, not yet **PRODUCTION READY**.

---

## 2. Test Reproducibility & State Hermeticity (Audit Section 1)

### Audit Criteria
1. Backend test suite executes cleanly multiple times without flakiness.
2. E2E verification executes cleanly multiple times without manual intervention.
3. Fresh isolated test databases are used; development and production databases remain untouched.
4. No background processes remain bound to ports after execution.
5. Failed assertions reliably return non-zero exit codes.

### Execution Evidence
- **Backend Pytest Suite (`pytest backend/tests -v`)**:
  - Run 1: **35 passed in 5.23s** (Exit Code 0).
  - Run 2: **35 passed in 4.20s** (Exit Code 0).
  - Test count: Exactly 35 unit, integration, and scenario tests.
- **Automated E2E Verification (`python scripts/verify_e2e.py`)**:
  - Run 1: **14/14 stages passed** (Exit Code 0).
  - Run 2: **14/14 stages passed** (Exit Code 0).
  - Uses isolated database: `backend/test_e2e_isolated.db` (automatically cleaned up in `finally:` block).
  - Server lifecycle: Ephemeral `uvicorn` instance spawned on dedicated port 8005 and terminated cleanly.
- **Port Teardown Verification**:
  - Command: `Get-NetTCPConnection -LocalPort 8000, 8005`
  - Output: `0 active connections`. Zero orphaned processes.
- **Development Database Preservation**:
  - `backend/sutra_learn.db` was verified before and after test runs. Size (106,496 bytes) and timestamp remained intact.
- **Assertion Exit Code Verification**:
  - `scripts/verify_e2e.py`: `if not all_passed: sys.exit(1)` ensures any single stage failure terminates with exit code 1.

**Classification:** **VERIFIED**

---

## 3. AI Provider & Transparent Fallback (Audit Section 2)

### Implementation Audit: [`backend/app/ai/provider.py`](file:///c:/Users/Yash/OneDrive/Desktop/Sutra_Learn/backend/app/ai/provider.py)

#### 1. Supported Model Identifier
- The actual model identifier in code is `gemini-2.5-flash` (configurable via `AI_MODEL` environment variable, defaulting to `gemini-2.5-flash` in `provider.py` lines 246 & 370).
- *Discrepancy Noted*: Previous documentation (`docs/ai-tutor-architecture.md`) claimed `gemini-1.5-flash`. The codebase uses `gemini-2.5-flash`.

#### 2. Provider Endpoint & Request Structure
- Endpoint: `https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}`
- Payload structure conforms to Google Generative Language v1beta:
  - `contents`: Array of role/parts objects preserving conversation history (`user` / `model`).
  - `systemInstruction`: Strict pedagogical role definition with NCERT Class 8 context.
  - `generationConfig`: `temperature: 0.4`, `maxOutputTokens: 800`.

#### 3. Credential & Error Handling
- **Missing Credentials**: `get_ai_provider()` inspects `GEMINI_API_KEY`. If unset, empty, or mock (`mock_*`, `your_*`), it immediately returns `CurriculumGroundedFallbackProvider()` without network attempts.
- **Invalid Credentials**: When tested with `api_key="invalid_key_test_123"`, the remote service returns HTTP 400. `GeminiProvider.generate_tutor_response()` catches `res.status_code != 200`, logs a warning, and immediately returns a curriculum-grounded fallback response with `fallback_reason: "Gemini API unavailable; serving grounded curriculum response."`.
- **Timeouts**: Configured with `httpx.AsyncClient(timeout=12.0)` for tutor chat and `timeout=15.0` for educator insights.

#### 4. Real Conversation Demonstration (Curriculum Fallback Engine)
*Because `GEMINI_API_KEY` is not populated in this offline audit environment, live AI was not fabricated. The system transparently executed via the Curriculum Fallback:*

- **Inquiry**: `"How do I isolate x in 2x + 5 = 15?"` (Concept: `MATH-C05`)
- **Mode**: `guided_learning`
- **Output**:
  > *"Whenever you modify an algebraic equation, balance must be preserved on both sides. For example, in $$2x + 5 = 15$$, our goal is to isolate $$x$$. What do you think is the first logical step to isolate the term $$2x$$?"*
- **Progressive Hints**:
  - *Tier 1*: `"Look at what is added to 2x. How can we undo adding 5?"`
  - *Tier 2*: `"Subtract 5 from both sides of the equation."`
- **Follow-Up Turn**: `"I subtracted 5 to get 2x = 10"`
- **Response**: Explains inverse operation of multiplication ($2 \cdot x = 10 \implies x = 10 / 2 = 5$) and prompts for substitution check.

**Classification:** **VERIFIED**

---

## 4. Mathematical Integrity & Algebraic Problem-Solving (Audit Section 3)

### Independent Verification Script: [`scripts/verify_mathematics.py`](file:///c:/Users/Yash/OneDrive/Desktop/Sutra_Learn/scripts/verify_mathematics.py)

The 8 core mathematical capabilities required by the audit directive were tested independently of language models:

| Test Case | Mathematical Expression | Algebraic Solution Steps | Verification by Substitution | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Case 1** | $2x + 5 = 15$ | $2x = 10 \implies x = 5$ | $\text{LHS} = 2(5) + 5 = 15 = \text{RHS}$ | **PASS** |
| **Case 2** | $3x - 7 = 11$ | $3x = 18 \implies x = 6$ | $\text{LHS} = 3(6) - 7 = 11 = \text{RHS}$ | **PASS** |
| **Case 3** | $2(x + 3) = 14$ | $2x + 6 = 14 \implies 2x = 8 \implies x = 4$ | $\text{LHS} = 2(4 + 3) = 14 = \text{RHS}$ | **PASS** |
| **Case 4** | $5x + 2 = 3x + 10$ | $2x = 8 \implies x = 4$ | $\text{LHS} = 5(4) + 2 = 22 = 3(4) + 10 = \text{RHS}$ | **PASS** |
| **Case 5A**| $-4x + 9 = 29$ | $-4x = 20 \implies x = -5$ | $\text{LHS} = -4(-5) + 9 = 29 = \text{RHS}$ | **PASS** |
| **Case 5B**| $-7x = 35$ | $x = 35 / (-7) \implies x = -5$ | $\text{LHS} = -7(-5) = 35 = \text{RHS}$ | **PASS** |
| **Case 6** | Sign Error Trap | $2x + 5 = 15 \to 2x = 20$ | Tagged `SIGN_ERROR` in question bank | **PASS** |
| **Case 7** | Inverse Division Trap | $4x = 28 \to x = 112$ | Tagged `INVERSE_OPERATION_CONFUSION` | **PASS** |
| **Case 8** | Substitution Check | $3x + 5 = 2x + 9$ | Evaluates $x=4 \implies \text{LHS} = 17, \text{RHS} = 17$ | **PASS** |

### Adaptive Engine Response to Mathematical Traps
- **Sign Error Clustering**: When 2 consecutive sign errors are submitted on linear equations, the adaptive engine deterministically triggers `BRIDGE_BACK` to prerequisite `MATH-C01` (Integer Arithmetic).
- **Persistent Error**: When 3 distinct failures occur without resolution, the engine deterministically pauses progression and triggers `TEACHER_REVIEW`.
- **Mastery**: When 2 distinct questions are solved unassisted with $\ge 85\%$ accuracy, the engine triggers `STRETCH`.

**Classification:** **VERIFIED**

---

## 5. Authentication & Security Threat Model (Audit Section 4)

### Implementation Audit: [`backend/app/auth.py`](file:///c:/Users/Yash/OneDrive/Desktop/Sutra_Learn/backend/app/auth.py)

#### 1. Cryptographic Token Format
- Token format: `sutra.<base64url_payload>.<sig_b64>`
- Secret: Reads `SUTRA_SECRET_KEY` environment variable (with development fallback key).
- Signature algorithm: `HMAC-SHA256` computed over `payload_b64`.
- Verification: Uses `hmac.compare_digest` to eliminate timing side-channel attacks.

#### 2. Expiration & Tampering
- Expiration: Fixed 24-hour lifetime (`TOKEN_EXPIRY_SECONDS = 86400`). Expired tokens throw `401 Unauthorized`.
- Tampering: Altering any character in payload or signature fails signature recomputation and throws `401 Unauthorized`.

#### 3. Role Enforcement & Resource Ownership
- `require_teacher` dependency rejects students with `403 Forbidden` on `/api/v1/teacher/*`.
- `/api/v1/learners/{id}/progress` checks `current_user["id"] == learner_id` (or teacher), rejecting cross-student access with `403 Forbidden`.
- `/api/v1/attempts` checks `current_user["id"] == attempt.learner_id`, preventing spoofed student submissions.
- `/api/v1/tutor/conversations/{id}` checks `conv["user_id"] == current_user["id"]`, preventing students from reading or deleting peers' tutor conversations.

#### 4. Frontend Route Guard Vulnerability Discovered & Corrected
- **Defect Found During Audit**: In `frontend/src/App.tsx`, lines 263–274 contained a development fallback: when an unauthenticated user or student navigated to `/teacher/dashboard`, the code automatically forged a teacher session for `teacher-01` via `authenticatePersona`.
- **Remediation Implemented**: Removed automatic persona creation. Replaced with strict route guards:
  - When `route.type === 'teacher'` and `stored?.role !== 'teacher'`, immediately calls `navigate('/teacher/login')`.
  - When `route.type === 'student'` and `stored?.role !== 'student'`, immediately calls `navigate('/student/login')`.
- **Regression Verified**: Playwright automated test confirmed: when a student navigates to `/teacher/dashboard`, they are immediately redirected to `/teacher/login`.

#### 5. Untested Security Risks & Production Gaps
1. **No Application Rate Limiting**: The FastAPI backend lacks route-level rate limiting (e.g. `slowapi` or Redis token buckets). While assessment idempotency keys prevent score inflation, the `/api/v1/tutor/chat` and `/api/v1/auth/session` endpoints are vulnerable to request spamming.
2. **Hardcoded Fallback Secret**: `SUTRA_SECRET_KEY` in `backend/app/auth.py` contains a default development fallback string. In production, this must be enforced via an environment variable assertion at startup.

**Classification:** **VERIFIED (WITH IDENTIFIED PRODUCTION GAPS)**

---

## 6. BKT Implementation vs. Reality Analysis (Audit Section 5)

### Major Discrepancy Analysis

The previous report claimed:
> *"The adaptive scoring engine is implemented in backend/app/engine/scorer.py and recommender.py using Bayesian Knowledge Tracing with P(L_0)=0.15, P(T)=0.20, P(G)=0.20, P(S)=0.10."*

### Reality in Source Code
1. **Files**: `backend/app/engine/scorer.py` and `recommender.py` **do not exist**. The actual engine files are [`backend/app/engine/adaptive.py`](file:///c:/Users/Yash/OneDrive/Desktop/Sutra_Learn/backend/app/engine/adaptive.py) and [`backend/app/engine/policy.py`](file:///c:/Users/Yash/OneDrive/Desktop/Sutra_Learn/backend/app/engine/policy.py).
2. **Algorithm**: The actual engine does **not** execute Bayesian probabilistic Markov updates ($P(L_t \mid C) = \dots$). Instead, it uses a **deterministic pedagogical policy engine**:
   - Distinct item evaluation: Multiple attempts at the same question are deduplicated (`total_distinct = len(distinct_attempts)`).
   - Weighted score formula:
     $$\text{weighted\_score} = \frac{\text{unassisted\_correct} \cdot 1.0 + \text{assisted\_correct} \cdot \text{hint\_penalty\_factor}}{\text{total\_distinct}}$$
   - Policy parameters in `AdaptivePolicyConfig`:
     - `min_attempts_for_mastery = 2`
     - `mastery_accuracy_threshold = 0.85`
     - `scaffold_accuracy_threshold = 0.50`
     - `max_consecutive_errors_before_review = 3`
     - `hint_penalty_factor = 0.5`
   - Misconception mapping: Direct lookup `MISCONCEPTION_TO_PREREQUISITE_MAP` triggering `BRIDGE_BACK`.
3. **Calibrated vs. Default**: The values in `policy.py` are sensible heuristic defaults ($85\%$ for mastery, $50\%$ for scaffold, $50\%$ weight for hint assistance), not empirically calibrated on live psychometric data.
4. **AI Independence**: Confirmed 100%. The AI Tutor and Educator Assistant have **zero write access** to the `concept_progress`, `attempts`, or `recommendations` tables. Progress updates occur exclusively via `crud.record_attempt()` and `crud.save_recommendation()`.

**Classification:** **PARTIALLY VERIFIED (Engine is fully functional, deterministic, and reliable, but is rule-based, not Bayesian).**

---

## 7. Frontend Interaction Verification via Browser Automation (Audit Section 6)

### Automation Driver: Playwright + Google Chrome (`scripts/verify_frontend_interactions.py`)

Every required interaction was executed against live ephemeral instances of the backend (port 8000) and frontend preview (port 5173):

| Test ID | Interaction Description | Viewport | Verified Behavior | Status |
| :--- | :--- | :--- | :--- | :--- |
| **UI-01** | Root Gateway Loading | 1440px | Earthbound Editorial wordmark & dual gateways render | **PASS** |
| **UI-02** | Student Login (`student-01`) | 1440px | Submits credentials, receives token, routes to `/student/home` | **PASS** |
| **UI-03** | Protected Navigation Guard | 1440px | Student attempting `/teacher/dashboard` redirected to `/teacher/login` | **PASS** |
| **UI-04** | Lesson Content Loading | 1440px | Loads NCERT lesson text, worked steps, and comprehension check | **PASS** |
| **UI-05** | Assessment Interactive Submission | 1440px | Selects radio option, clicks Check Answer, receives feedback | **PASS** |
| **UI-06** | Student Progress View | 1440px | Displays concept progress bars and mastery percentage | **PASS** |
| **UI-07** | AI Tutor Socratic Message | 1440px | Types prompt, receives Socratic guiding response with hints | **PASS** |
| **UI-08** | AI Tutor Multi-Turn Follow-Up | 1440px | Sends intermediate working, receives verification turn | **PASS** |
| **UI-09** | Student Logout | 1440px | Clears token from localStorage, returns to gateway `/` | **PASS** |
| **UI-10** | Teacher Login (`teacher-01`) | 1440px | Submits credentials, receives teacher token, routes to dashboard | **PASS** |
| **UI-11** | Educator Cohort Dashboard | 1440px | Renders cohort student summaries and accuracy rates | **PASS** |
| **UI-12** | Educator AI Assistant Canvas | 1440px | Clicks preset query, receives 4-level evidence hierarchy | **PASS** |
| **UI-13** | Teacher Intervention Confirmation | 1440px | Enters clinical rationale ($\ge 5$ chars), submits override | **PASS** |
| **UI-14** | Audit Trail Verification | 1440px | Renders override record with SHA-256 state hash | **PASS** |
| **UI-15** | Teacher Logout | 1440px | Clears session, returns to gateway `/` | **PASS** |
| **UI-16** | Mobile Gateway Responsive Load | 390px | Layout scales to single column without horizontal overflow | **PASS** |
| **UI-17** | Mobile Student Login Flow | 390px | Touch inputs and submit button fully operable | **PASS** |
| **UI-18** | Mobile AI Tutor Canvas | 390px | Tutor chat input and messages fit within 390px viewport | **PASS** |
| **UI-19** | Mobile Teacher Navigation | 390px | Educator shell stacks cleanly on mobile screen | **PASS** |

**Summary Result:** **19/19 PASSED (100% Interactive Coverage)**

**Classification:** **VERIFIED**

---

## 8. Deployment Readiness (Audit Section 7)

### Configuration Audit

#### 1. Backend (`render.yaml`)
- `buildCommand: "pip install -r backend/requirements.txt"`
- `startCommand: "cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT"`
- `healthCheckPath: /api/v1/health` verified.
- `disk`: Persistent disk mounted at `/var/data` (1 GB) for SQLite persistence.
- `SUTRA_DB_PATH: /var/data/sutra_learn.db` correctly references persistent disk.

#### 2. Frontend (`frontend/vercel.json`)
- `buildCommand: "npm run build"`
- `outputDirectory: "dist"`
- `rewrites: [{"source": "/(.*)", "destination": "/index.html"}]` provides SPA pushState routing.

#### 3. Database Initialization & Migrations
- `lifespan(app)` invokes `init_db()`.
- Tables created with `CREATE TABLE IF NOT EXISTS` and seeded on first run.
- *Remaining Risk*: No automated database migration tool (such as Alembic) is configured for SQLite schema evolution.

#### 4. Live Cloud Deployment Status
- No live cloud deployment was executed or claimed during this audit.
- Readiness is verified through static configuration and local production preview simulation (`npx vite preview` + `uvicorn`).

**Classification:** **PARTIALLY VERIFIED (Configurations are complete and verified in preview, but live cloud deployment was not executed).**

---

## 9. Comprehensive Audit Claim Matrix

| Claim from Previous Report | Source Location | Audit Method | Verified Result | Audit Classification |
| :--- | :--- | :--- | :--- | :--- |
| **35/35 Backend Pytest Passing** | `backend/tests/` | Ran `pytest` twice | 35 passed in 4.20s | **VERIFIED** |
| **14/14 Hermetic E2E Stages Passing** | `scripts/verify_e2e.py` | Ran script twice | 14/14 passed with Code 0 | **VERIFIED** |
| **Oxlint Zero Warnings / Errors** | `frontend/` | Ran `oxlint` | 0 errors, 0 warnings (171ms) | **VERIFIED** |
| **Frontend Production Build Clean** | `frontend/dist/` | Ran `vite build` | Clean bundle (96.7 kB gzip) | **VERIFIED** |
| **48/48 Multi-Device Screenshots** | `screenshots/` | Chrome headless capture | 48 files verified across 3 viewports | **VERIFIED** |
| **Dual-Portal Unbreachable Separation** | `frontend/src/App.tsx` | Playwright route testing | Redirects unauthorized roles | **VERIFIED** |
| **Cryptographic HMAC-SHA256 Auth** | `backend/app/auth.py` | Timing-safe token test | Signatures verified, spoofing blocked | **VERIFIED** |
| **Cross-Student IDOR Protection** | `backend/app/auth.py` | Pytest & E2E Stage 10 | Returns 403 Forbidden | **VERIFIED** |
| **Mandatory Clinical Rationale ($\ge 5$ chars)**| `backend/app/routers/teacher.py`| E2E Stage 11 & Pytest | Empty/short reason throws 400 | **VERIFIED** |
| **NCERT Class 8 Curriculum Graph (DAG)**| `backend/app/content/` | Topological sort test | 6 concepts, strictly acyclic | **VERIFIED** |
| **8 Core Algebraic Equations Solved** | `scripts/verify_mathematics.py` | Independent solver test| All 8 equations and substitutions verified | **VERIFIED** |
| **SUTRA AI Personal Mathematics Tutor** | `backend/app/routers/tutor.py`| Playwright & Pytest | 6 modes, progressive hints, history | **VERIFIED** |
| **Curriculum Fallback Engine** | `backend/app/ai/provider.py` | Unit & live chat test | Grounded, deterministic, offline-ready | **VERIFIED** |
| **4-Level Educator Evidence Hierarchy** | `EducatorAssistant.tsx` | Playwright test UI-12 | Facts, Stats, Insights, Actions rendered | **VERIFIED** |
| **Cartesian Join Row Multiplication Fixed**| `backend/app/db/crud.py` | Query inspection & E2E | Independent subqueries, acc $\le 100\%$ | **VERIFIED** |
| **SQLite WAL Pragma Deadlock Fixed** | `backend/app/db/database.py`| Concurrent conn test | WAL set once in `init_db()`, 0 timeouts | **VERIFIED** |
| *Bayesian Knowledge Tracing (BKT)* | `backend/app/engine/` | Code inspection | Rule-based policy engine, not Bayesian | **PARTIALLY VERIFIED** |
| *File Paths in Report (`scorer.py`)* | `backend/app/engine/` | File search | Files are `adaptive.py` and `policy.py` | **FAILED (Report Inaccuracy)** |
| *Live Cloud Deployment* | Staging environments | Infrastructure check | Configs ready; no live deploy tested | **NOT VERIFIED** |

---

## 10. Final Release Decision & Actionable Roadmap

### Official Decision: **RELEASE CANDIDATE (RC 1.0.0 APPROVED FOR STAGING)**

The codebase demonstrates exceptional engineering quality, deterministic mathematical reliability, clean dual-portal role segregation, and an interactive, responsive user experience. The previous defects (E2E socket crashes, WAL pragma deadlocks, cross-portal bypasses, and Cartesian join bugs) have been resolved at the root cause.

### Required Actions Prior to Production Release (v1.0.0-PROD)
1. **Application Rate Limiter**: Install `slowapi` or Redis-backed rate limiting on `/api/v1/tutor/chat` (e.g. 20 requests/minute) and `/api/v1/auth/session` (e.g. 10 requests/minute).
2. **Production Secret Enforcement**: Assert that `SUTRA_SECRET_KEY` is set and does not match the default development string during backend startup.
3. **Staging Smoke Test on Render & Vercel**: Deploy to Render and Vercel staging environments and execute `verify_frontend_interactions.py` against the live URLs.
4. **Documentation Alignment**: Correct references in technical docs to cite `backend/app/engine/adaptive.py` and describe the algorithm accurately as a *Deterministic Evidence-Weighted Policy Engine*.

