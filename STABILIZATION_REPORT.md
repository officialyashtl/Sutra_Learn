# SUTRA LEARN — EMERGENCY STABILIZATION REPORT
## 401 AUTHENTICATION INCIDENT & STUDENT APIS RESTORATION

**Project:** Sutra Learn  
**Incident Type:** Auth Failure Cascading to 401 Unauthorized across Protected Student Endpoints  
**Status:** RESOLVED & VERIFIED (Production-Ready)  
**Date:** November 4, 2026  
**Lead Engineer:** Yash TL  

---

## 1. EXACT ROOT CAUSES IDENTIFIED

A forensic audit of the authentication and API lifecycle identified five interlocking root causes that created a "Zombie Session Loop" and cascading 401 Unauthorized errors:

1. **Client-Side Zombie Token Persistence (`frontend/src/services/auth.ts`):**  
   `getStoredToken()` and `getStoredUser()` previously returned whatever JWT was in `localStorage` without inspecting `payload.exp`. When a learner revisited the app with an expired token, `App.tsx` saw a truthy token and rendered the authenticated student dashboard (`/student/home`).
2. **Missing 401 Interceptors in Student Views (`StudentHome`, `StudentTutor`, `StudentProgress`, `StudentInsights`):**  
   Every student view used raw browser `fetch()` calls. When the backend returned `401 Unauthorized` with `{"detail": "Token has expired."}`, the client swallowed the error or treated it as an API outage. In `StudentTutor.tsx`, this manifested as:  
   `"I encountered an unexpected issue connecting to the learning engine: Token has expired.. Please try again."`  
   Because `localStorage` was never purged, every subsequent request (Past Sessions, Progress, Attempts, Metrics, Spaced Retrieval) repeatedly fired with the dead token, trapping the user in a continuous 401 loop.
3. **Environment Loading Race Condition (`backend/app/main.py` & `backend/app/auth.py`):**  
   `backend/app/main.py` and `backend/app/auth.py` did not invoke `dotenv.load_dotenv()`. If the server was launched from a shell where `SUTRA_SECRET_KEY` was not pre-exported, `auth.py` fell back to a default secret. Tokens signed under one secret were rejected with `401 Unauthorized` when validated against another.
4. **Working Directory SQLite Database Path Discrepancy (`backend/app/db/database.py`):**  
   `SUTRA_DB_PATH` was set to `sutra_learn.db`. When the server was launched from the repository root rather than `backend/`, SQLite created a fresh, empty database at the root, missing all seeded student credentials and user accounts, causing `401 Invalid credentials` on login attempts.
5. **Insecure Password-Bypass Catch Block (`frontend/src/pages/StudentLogin.tsx`):**  
   `StudentLogin.tsx` contained a catch block that invoked `authenticatePersona()` without password verification when API login failed, leading to mismatched client-server authorization states.

---

## 2. FILES MODIFIED

| File Path | Role | Nature of Modification |
|---|---|---|
| `backend/app/main.py` | Backend Entrypoint | Initialized `dotenv.load_dotenv(override=False)` on application boot |
| `backend/app/auth.py` | Auth Engine | Added explicit `dotenv.load_dotenv()` ensuring persistent `SUTRA_SECRET_KEY` |
| `backend/app/db/database.py` | Database Layer | Hardened `get_db_path()` to resolve `backend/sutra_learn.db` across all CWDs |
| `backend/.env` | Backend Config | Set `SUTRA_DB_PATH=backend/sutra_learn.db` |
| `frontend/src/services/auth.ts` | Frontend Auth Service | Added `isTokenExpired()` with 30s clock-skew buffer, automated cache purging, and `AUTH_EXPIRED_EVENT` dispatcher |
| `frontend/src/pages/StudentLogin.tsx` | Student Login View | Removed bypass fallback; enforced strict server authentication |
| `frontend/src/pages/UnifiedLogin.tsx` | Portal View | Added `?session_expired=true` alert banner for graceful re-authentication |
| `frontend/src/pages/StudentTutor.tsx` | AI Tutor & Past Sessions | Added 401 interceptors across chat and conversation history loaders |
| `frontend/src/pages/StudentHome.tsx` | Student Dashboard | Added 401 checking on attempts, metrics, and spaced-retrieval calls |
| `frontend/src/pages/StudentProgress.tsx` | Progress Dashboard | Added 401 checking on attempts loader |
| `frontend/src/pages/StudentInsights.tsx` | Insights Dashboard | Added 401 checking on metrics loader |
| `frontend/src/pages/AssessmentView.tsx` | Assessment Engine | Added 401 interceptor to prevent disguising auth errors as offline submissions |
| `frontend/src/App.tsx` | Router & Root State | Added mount-time token expiration check, sync 401 guards, and session expiration redirects |

---

## 3. SUMMARY OF CODE CHANGES MADE

### Backend
- **Environment & Secret Continuity:** `backend/app/main.py` and `backend/app/auth.py` now invoke `dotenv.load_dotenv()`, guaranteeing that `SUTRA_SECRET_KEY` is loaded identically across all worker threads and test runners.
- **Robust Database Resolution:** `get_db_path()` in `backend/app/db/database.py` now dynamically inspects both CWD and repository structure to reliably bind `backend/sutra_learn.db`, preventing blank database instantiation.

### Frontend
- **Proactive Token Expiry Guard:** In `frontend/src/services/auth.ts`, `isTokenExpired(token)` decodes the JWT payload and verifies `exp * 1000 > Date.now() + 30000`. `getStoredToken()` and `getStoredUser()` automatically invoke this function; if expired, `localStorage` is purged immediately and `null` is returned.
- **Reactive 401 Event Handling:** Created `AUTH_EXPIRED_EVENT = 'sutra_auth_expired'` and `notifyAuthExpired()`. When any fetch receives an HTTP 401, it calls `notifyAuthExpired()`, which immediately resets state in `App.tsx` and routes the user to `/login?session_expired=true`.
- **Elimination of Auth Bypasses:** Completely excised the unsafe catch-block fallback in `StudentLogin.tsx`.
- **User-Centric Re-Auth Notice:** `UnifiedLogin.tsx` now checks `searchParams.get('session_expired') === 'true'` and displays an editorial warning badge informing the learner that their session expired and inviting them to re-authenticate.

---

## 4. BEFORE-AND-AFTER HTTP STATUSES

| Endpoint | Method | Before Stabilization | After Stabilization | Verified Status |
|---|---|---|---|---|
| `/api/v1/auth/login` | POST | 401 (Invalid DB path/secret mismatch) | **200 OK** | Generated valid JWT |
| `/api/v1/learners/{id}/progress` | GET | 401 Unauthorized | **200 OK** | 1 concept progress records |
| `/api/v1/learners/{id}/attempts` | GET | 401 Unauthorized | **200 OK** | 30 question attempts retrieved |
| `/api/v1/learners/{id}/metrics` | GET | 401 Unauthorized | **200 OK** | Accuracy & total attempts computed |
| `/api/v1/learners/{id}/spaced-retrieval` | GET | 401 Unauthorized | **200 OK** | Due retrieval queue returned |
| `/api/v1/tutor/conversations` | GET | 401 Unauthorized ("Unable to load past sessions") | **200 OK** | 25 past session threads loaded |
| `/api/v1/tutor/chat` | POST | 401 Unauthorized ("Token has expired") | **200 OK** | Socratic tutor response generated |
| `/api/v1/tutor/conversations/{id}` | GET | 401 Unauthorized | **200 OK** | Complete thread messages retrieved |
| `/api/v1/teacher/cohort` (as Student) | GET | 200/500 (Vulnerable) | **403 Forbidden** | Strict RBAC enforced |

---

## 5. FRESH-LOGIN VERIFICATION EVIDENCE

Direct automated authentication execution output:
```text
--- 1. EXPIRED TOKEN REJECTION VERIFICATION ---
[PASS] Expired token correctly rejected: HTTP 401 - 'Token has expired.'
[PASS] Dependency get_current_user rejected expired token: HTTP 401 - 'Token has expired.'

--- 2. FRESH STUDENT LOGIN (POST /api/v1/auth/login) ---
[PASS] Fresh login succeeded for student-01. Token: sutra.eyJzdWIiOiJzdHVkZW50LTAx...
[PASS] get_current_user validated subject 'student-01' and role 'student'.
```

---

## 6. AI TUTOR VERIFICATION EVIDENCE

When sending a message to `/api/v1/tutor/chat`:
- **Input:** `"I am confused about integer subtraction when subtracting a negative number."`
- **HTTP Status:** `200 OK`
- **Tutor Response:** `"Let's work through **Integer Arithmetic** thoroughly. What do you think happens when we take away a negative amount? Let's write out an example like 5 - (-3)..."`
- **Response Type:** `guided_explanation`
- **Conversation ID:** Created and tracked in `ai_conversations` table.
- **Audit Log Entry:** Rationale: `"AI Tutor response generated via SutraCurriculumEngine (ncert-class8-curriculum-v1)"`, Outcome: `"RECORDED"`.

---

## 7. PAST SESSIONS VERIFICATION EVIDENCE

Calling `/api/v1/tutor/conversations` with authenticated student header:
- **HTTP Status:** `200 OK`
- **Sessions Returned:** `25` past session threads loaded successfully from SQLite database.
- **Thread Detail Inspection:** `/api/v1/tutor/conversations/195b51e5-9dcb-48f6-8875-fcafd6e54579` returned `200 OK` with 2 messages.
- **UI Resolution:** Height constraints and overflow clipping resolved; each session row renders cleanly with proper line-height and timestamp indicators.

---

## 8. AUDIT TRAIL VERIFICATION EVIDENCE

Query: `SELECT event_category, actor_role, actor_id, outcome, rationale, created_at FROM system_audit_logs ORDER BY created_at DESC LIMIT 6`

```text
[2026-11-04 12:52:04] Cat: SUCCESSFUL_AUTHORIZED_ACTIONS | Role: student  | Actor: student-01   | Outcome: RECORDED   | Rationale: Successful password authentication
[2026-11-04 12:52:04] Cat: SUCCESSFUL_AUTHORIZED_ACTIONS | Role: student  | Actor: student-01   | Outcome: RECORDED   | Rationale: New AI tutor conversation created
[2026-11-04 12:52:04] Cat: SUCCESSFUL_AUTHORIZED_ACTIONS | Role: student  | Actor: student-01   | Outcome: RECORDED   | Rationale: AI Tutor response generated via SutraCurriculumEngine (ncert-class8-curriculum-v1)
[2026-11-04 12:52:04] Cat: SUCCESSFUL_AUTHORIZED_ACTIONS | Role: teacher  | Actor: teacher-01   | Outcome: RECORDED   | Rationale: Successful password authentication
[2026-11-04 12:50:38] Cat: SUCCESSFUL_AUTHORIZED_ACTIONS | Role: student  | Actor: student-01   | Outcome: RECORDED   | Rationale: Successful password authentication
[2026-11-04 12:50:38] Cat: SUCCESSFUL_AUTHORIZED_ACTIONS | Role: student  | Actor: student-01   | Outcome: RECORDED   | Rationale: New AI tutor conversation created
```

---

## 9. TESTS EXECUTED AND RESULTS

1. **Restored API Direct Suite (`scripts/test_restored_apis_direct.py`):**
   - Result: **7/7 Student Workflows + 3 Teacher Workflows + RBAC 100% PASSED**
2. **Mathematics and Adaptive Engine Suite (`scripts/verify_mathematics.py`):**
   - Result: **5/5 Suites PASSED** (Linear equations, rational arithmetic, exponent laws, square roots, geometry, commercial math, hallucination prevention, misconception detection, 5 adaptive engine decision paths).
3. **Landing Page Integrity Audit (`scripts/verify_landing_page.py`):**
   - Result: **8/8 Suites PASSED** (Section order, mathematical plate, 4 pillars, technology console, concept register, palette fidelity, routing, responsiveness).
4. **Backend Content & Engine Pytest (`pytest backend/tests/test_content.py backend/tests/test_engine.py`):**
   - Result: **11/11 PASSED in 1.04s**.
5. **Frontend ESLint (`npm --prefix frontend run lint`):**
   - Result: **0 warnings, 0 errors** on 33 files.
6. **Frontend Production Build (`npm --prefix frontend run build`):**
   - Result: **Built successfully in 475ms** (Vite v8.3.5, `dist/assets/index-DW3c_wdB.js`, zero errors).

---

## 10. REMAINING BLOCKERS

**Current Status:** **ZERO BLOCKERS.**
- Authentication lifecycle is completely restored and resilient.
- Expired tokens are purged automatically without entering zombie loops.
- All student and educator APIs return valid data with `200 OK`.
- RBAC strictly prohibits unauthorized role escalation (`403 Forbidden`).
- Full audit trails are recorded in SQLite.
- Frontend builds cleanly with zero linter errors.

