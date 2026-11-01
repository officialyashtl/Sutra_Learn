# SUTRA LEARN — Product Gap Analysis & Quality Audit

> Assessment date: 2026-10-29  
> Target: Class 8 Mathematics (Linear Equations & Prerequisites)  
> Audit scope: UI/UX, Learning Science, Adaptive Intelligence, API/DB Security, QA

---

## The 10 Highest-Impact Defects Identified

### 1. Insecure Default Header in Teacher Endpoints (Authorization Bypass)
- **Affected File**: `backend/app/routers/teacher.py`
- **Defect Description**: The endpoints `/api/v1/teacher/cohort` and `/api/v1/teacher/overrides` use `x_teacher_id: str = Header(default="teacher-01")`. An unauthenticated caller omitting the header is automatically assigned administrative teacher privileges (`teacher-01`).
- **Reproducible Scenario**: `curl -X GET http://127.0.0.1:8000/api/v1/teacher/cohort` without headers returns 200 OK and confidential student diagnostic records.
- **Remediation**: Require `x-teacher-id` without default; validate existence and `role == 'teacher'` in SQLite. Return `401/403` for missing/unauthorized credentials.

### 2. Unrestricted Learner Data Access (Resource Ownership Leak)
- **Affected File**: `backend/app/routers/learners.py`
- **Defect Description**: `/api/v1/learners/{learner_id}/attempts` and `/progress` accept any `learner_id` without checking the caller's identity. Any student can inspect other learners' private attempts and diagnostics.
- **Reproducible Scenario**: Student `student-01` queries `/api/v1/learners/student-02/attempts` and views all answers and misconception tags of `student-02`.
- **Remediation**: Enforce `x-user-id` header validation; allow access only if `x-user-id == learner_id` or `x-user-id` is an authorized teacher.

### 3. Sparse Question Bank (&lt; 5 Questions per Concept)
- **Affected File**: `backend/app/content/questions.py`
- **Defect Description**: Concepts currently contain only 2 questions each (total 11 questions). Because the adaptive engine requires at least 2 distinct items for evaluation, students immediately exhaust the question bank upon retry.
- **Reproducible Scenario**: Student takes `MATH-C01` assessment twice; on third attempt, no unattempted diagnostic questions exist.
- **Remediation**: Expand question bank to &ge; 5 distinct, mathematically verified questions per concept (30+ questions total), spanning foundational, procedural, conceptual, and transfer demands.

### 4. Client-Side Concept Unlock without Prerequisite Enforcement
- **Affected File**: `frontend/src/pages/StudentHome.tsx`
- **Defect Description**: All concepts display active "Lesson" and "Practice" buttons regardless of whether the student has demonstrated prerequisite mastery. A student can jump straight to `MATH-C05` without ever attempting `MATH-C01`.
- **Reproducible Scenario**: A student with zero completed prerequisites clicks "Practice" on `MATH-C05` (Linear Equations) and receives advanced items without prerequisite check.
- **Remediation**: Implement backend and frontend prerequisite availability logic: lock concepts whose prerequisites are not yet completed/mastered; display clear educational lock banners explaining which prerequisite concept must be completed first.

### 5. Absence of Explicit Design System Tokens
- **Affected File**: `frontend/src/index.css`
- **Defect Description**: Styles currently use ad-hoc color variables rather than the mandated SUTRA LEARN design system specification (`--color-canvas: #f7f8fc`, `--color-primary: #5145cd`, `--color-secondary: #0f766e`, etc.).
- **Reproducible Scenario**: Visual inconsistencies across cards, buttons, badges, and focus rings; contrast variations across viewports.
- **Remediation**: Refactor CSS root tokens to the standardized design system and verify WCAG AA contrast (&ge; 4.5:1).

### 6. Missing State Machine Lifecycle in Question Assessment
- **Affected File**: `frontend/src/pages/AssessmentView.tsx`
- **Defect Description**: Question states are managed via loosely coupled boolean flags rather than an explicit lifecycle: `Ready → Answering → Submitted → Feedback → Next action`. This risks double submissions during network latency.
- **Reproducible Scenario**: Rapid clicking on "Submit" before request completes can submit duplicate requests if the client UUID is regenerated.
- **Remediation**: Refactor to an explicit lifecycle state enum; disable submission button while `status === 'Submitted'`; reuse stable attempt ID across retries.

### 7. Teacher Dashboard Missing Individual Student Evidence Inspector
- **Affected File**: `frontend/src/pages/TeacherDashboard.tsx`
- **Defect Description**: Teachers can see cohort aggregate numbers and trigger overrides, but cannot inspect a student's individual question attempts, timestamps, and diagnosed misconception breakdown.
- **Reproducible Scenario**: Teacher wants to know *why* student `student-01` was flagged with `TEACHER_REVIEW`, but the UI only provides the override form without granular attempt evidence.
- **Remediation**: Add a student detail modal/drawer displaying the student's attempt chronology, hint usage, error explanations, and concept mastery breakdown.

### 8. Lack of Explicit Offline Attempt Badge in Student Feedback
- **Affected File**: `frontend/src/pages/AssessmentView.tsx`
- **Defect Description**: When an attempt is queued offline in IndexedDB, the feedback card displays text but does not visually distinguish a "Locally Queued (Pending Sync)" status from a "Server-Confirmed" status.
- **Reproducible Scenario**: An offline student does not clearly see whether their mastery credit is officially recorded on the server or pending network restoration.
- **Remediation**: Add clear status badges: `[Locally Queued (Pending Sync)]` vs `[Server Confirmed]`, with live count of pending offline submissions in the assessment header.

### 9. Database Initialization Missing Schema Evolution / Migration Guard
- **Affected File**: `backend/app/db/database.py`
- **Defect Description**: `init_db()` executes `CREATE TABLE IF NOT EXISTS`, but does not verify foreign key pragma execution per connection session in multi-threaded contexts, and lacks an automated schema migration check.
- **Reproducible Scenario**: If a new column is added in future iterations, `CREATE TABLE IF NOT EXISTS` silently skips table modification.
- **Remediation**: Add explicit table schema verification on startup, ensuring WAL mode and `PRAGMA foreign_keys = ON;` are enforced on every database connection.

### 10. Automated Question Bank Validation Test Suite Missing
- **Affected File**: `backend/tests/test_content.py`
- **Defect Description**: Existing tests check that questions have options, but do not validate that distractors have unique text, that mathematical formulas evaluate correctly, or that cognitive demand distribution meets requirements across every concept.
- **Reproducible Scenario**: An author could add a question where distractor A and B have the same text or duplicate options, which would go unnoticed.
- **Remediation**: Implement a rigorous automated question bank audit test verifying minimum 5 questions per concept, unique option texts, valid misconception tags, non-empty hints, and full pedagogical explanation coverage.

