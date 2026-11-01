# SUTRA LEARN — Engineering Findings & Remediation Analysis

## 1. Executive Summary

During the forensic audit of SUTRA LEARN (Project Codename: SUTRA ASCENSION), four major categories of engineering friction were discovered that compromised the system's release readiness:
1. Recurring E2E test failures (`scripts/verify_e2e.py` returning exit code 1).
2. SQLite database deadlocks under high-frequency asynchronous execution.
3. Trust boundary bypass vulnerabilities via client-supplied headers.
4. Non-isolated test harness contaminating development state.

This document details the root causes identified, architectural remediation implemented, and verified outcomes.

---

## 2. Root Cause 1: E2E Verification Harness Fragility

### The Defect
When running `scripts/verify_e2e.py`, the test runner crashed with `ConnectionRefusedError: [WinError 10061]` or an unhandled exit code 1. Furthermore, duplicate submission idempotency tests failed with `AssertionError: 2 == 1`.

### Root Cause Analysis
1. **Unmanaged Server Lifecycle**: The test harness assumed an external `uvicorn` instance was manually started by a developer on port 8000. In automated CI/CD and sandboxed environments, no process was listening, triggering raw socket connection refusals.
2. **State Leakage & Collision**: The test used a hardcoded learner ID `duplicate-test-student`. If a previous test run failed or was aborted mid-flight, the record remained in the database. On subsequent runs, the count was 2 instead of 1, failing idempotency assertions.
3. **Database Contamination**: The test ran against `backend/sutra_learn.db`, colliding with development data and leaving orphaned assessment attempts.

### Remediation
1. **Self-Managed Ephemeral Server**: Rebuilt `scripts/verify_e2e.py` to spawn an isolated ephemeral `uvicorn` instance on dedicated port 8005.
2. **Dynamic Isolated Database**: Pointed the ephemeral instance to `backend/test_e2e_isolated.db` using the newly engineered `SUTRA_DB_PATH` environment override.
3. **Dynamic UUID Entity Keys**: Replaced hardcoded student and attempt keys with `uuid.uuid4().hex[:8]` prefixes, guaranteeing test hermeticity.
4. **Guaranteed Teardown**: Placed process termination, database file unlinking, and WAL/SHM file cleanup in a robust `finally:` block.

---

## 3. Root Cause 2: SQLite WAL Pragma Deadlock

### The Defect
Under concurrent request scenarios, endpoints hung indefinitely or timed out after 5.0 seconds.

### Root Cause Analysis
In SQLite, executing `PRAGMA journal_mode = WAL;` requires an **exclusive file lock**. In earlier code, `get_db_connection()` executed `conn.execute("PRAGMA journal_mode=WAL")` on **every single incoming request connection**. When one connection was actively reading or writing, a concurrent connection attempting to execute the WAL pragma was blocked, causing an SQLite database lock deadlock.

### Remediation
1. Configured WAL mode **strictly once** during database initialization in `init_db()`:
   ```python
   # backend/app/db/database.py
   with get_db_connection() as conn:
       conn.execute("PRAGMA journal_mode=WAL;")
   ```
2. In regular connection lifecycles (`get_db_connection()`), only light-weight connection-local pragmas are set:
   ```python
   conn.execute("PRAGMA busy_timeout = 5000;")
   conn.execute("PRAGMA foreign_keys = ON;")
   ```
3. Dynamically resolve DB path via `os.environ.get("SUTRA_DB_PATH", DEFAULT_DB_PATH)` to ensure complete process isolation during testing.

---

## 4. Root Cause 3: Identity Spoofing & Trust Boundary Inversion

### The Defect
Any caller could impersonate teachers or other students by simply adding headers:
- `x-teacher-id: teacher-01`
- `x-user-id: student-02`

### Root Cause Analysis
The original application trusted client headers for identity assertions. Looking up a teacher record in the database using a client-supplied ID validates that the ID exists; it does **not** validate that the client holds the authority of that identity.

### Remediation
1. **HMAC-SHA256 Token Issuance**: Built an authentication service (`/api/v1/auth/session` and `/api/v1/auth/login`) that issues cryptographically signed bearer tokens (`sutra.<payload>.<sig>`).
2. **Server-Side Token Verification**: Created FastAPI dependency `get_current_user` in `backend/app/auth.py`. Client headers `x-user-id` and `x-teacher-id` were completely removed from authorization logic.
3. **Role-Based Access Control (RBAC)**:
   - Educator endpoints require `role == "teacher"`.
   - Student endpoints restrict access to self-owned learner resources (`user_id == learner_id`).
   - Any violation triggers an immediate `401 Unauthorized` or `403 Forbidden`.

---

## 5. Root Cause 4: Cohort Analytics Cartesian Join Inflation

### The Defect
In `get_cohort_summary()` and `get_concept_analytics()`, accuracy calculations occasionally returned values exceeding 100% or miscalculated struggling learner counts.

### Root Cause Analysis
A multi-table `LEFT JOIN` between `learners`, `concept_progress`, and `attempts` generated a Cartesian product of rows whenever a student had multiple attempts on a concept. Aggregating `COUNT(attempts.id)` directly over this joined dataset resulted in inflated counts.

### Remediation
Restructured SQL queries in `backend/app/db/crud.py` to use independent aggregated subqueries:
```sql
SELECT 
    l.id AS learner_id,
    l.name,
    COALESCE(p_agg.mastered_count, 0) AS mastered_concepts,
    COALESCE(a_agg.total_attempts, 0) AS total_attempts,
    COALESCE(a_agg.correct_attempts, 0) AS correct_attempts,
    ROUND(
        CASE 
            WHEN COALESCE(a_agg.total_attempts, 0) > 0 
            THEN (CAST(a_agg.correct_attempts AS FLOAT) / a_agg.total_attempts) * 100.0 
            ELSE 0.0 
        END, 1
    ) AS cohort_accuracy
FROM learners l
LEFT JOIN (...) p_agg ON l.id = p_agg.learner_id
LEFT JOIN (...) a_agg ON l.id = a_agg.learner_id
WHERE l.role = 'student';
```
This guarantees mathematical accuracy bounds ($0\% \le \text{accuracy} \le 100\%$) and zero row multiplication.

---

## 6. Verification Summary

| Test Category | Suite / Script | Previous Result | Current Result |
| :--- | :--- | :--- | :--- |
| Backend Pytest | `pytest backend/tests` | Intermittent failures | **35/35 Passing (1.76s)** |
| E2E Verification | `python scripts/verify_e2e.py` | Exit code 1 (Crashed) | **14/14 Stages Passing (Code 0)** |
| Frontend Linter | `oxlint` | 5 Warnings | **0 Errors, 0 Warnings** |
| Frontend Bundler | `tsc -b && vite build` | Warnings / Untyped | **Clean Build (189ms)** |
| Visual Capture | `scripts/capture_screenshots.py` | 0/48 (No preview) | **48/48 Passing (Desktop/Tablet/Mobile)** |

