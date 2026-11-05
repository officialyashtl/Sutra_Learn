# SUTRA LEARN — End-to-End Product Walkthrough
### CodeKernel '26 Evaluator Guide & Interactive User Journey

This walkthrough provides a comprehensive tour of the live, operational **SUTRA LEARN** application. For each step, it records the exact URL/path, user action, system response, and references verified screenshot evidence available in `screenshots/`.

---

## Stage 1: Public Cover & Portal Gateway

| Attribute | Specification |
| :--- | :--- |
| **Path / URL** | `/` (`https://sutralearn.vercel.app/`) |
| **User Action** | Visitor navigates to root URL. |
| **System Behavior** | Renders the Earthbound Editorial cover page featuring curriculum highlights, interactive concept previews, pedagogical manifesto, and dual portal entry gates. |
| **Visual Evidence** | `screenshots/01_root_gateway_desktop.png` (Desktop), `01_root_gateway_tablet.png` (Tablet), `01_root_gateway_mobile.png` (Mobile) |

```
Key Screen Elements:
• Brand Header: SUTRA LEARN • NCERT Class 8 Mathematics
• Primary Action: "Start Learning" (routes to Student Gateway)
• Secondary Action: "Educator Portal" (routes to Teacher Gateway)
• Curriculum Preview: 30 Concepts mapped across NCERT chapters
```

---

## Stage 2: Dual-Portal Authentication

### 2.1 Student Gateway
- **Path:** `/student/login` (or `/login`)
- **Action:** Learner enters credentials or chooses a demo persona (`student-01` / `sutra123`).
- **Response:** Backend issues signed HMAC-SHA256 Bearer JWT with `role: "student"`. Client initializes `sessionStorage` and redirects to `/student/home`.
- **Evidence:** `screenshots/02_student_login_desktop.png`, `02_student_login_tablet.png`, `02_student_login_mobile.png`

### 2.2 Educator Gateway
- **Path:** `/teacher/login`
- **Action:** Faculty enters credentials (`teacher-01` / `teacher123`).
- **Response:** Backend validates credentials against PBKDF2 hash, issues token with `role: "teacher"`, and mounts the Educator Workspace Shell.
- **Evidence:** `screenshots/03_teacher_login_desktop.png`, `03_teacher_login_tablet.png`, `03_teacher_login_mobile.png`

---

## Stage 3: Student Experience

### 3.1 Student Hub (`/student/home`)
- **Action:** Student views personalized dashboard upon authentication.
- **Response:** Loads active concept progress cards, current mastery %, recent attempts, and prompt to continue learning.
- **Evidence:** `screenshots/04_student_home_desktop.png`, `04_student_home_tablet.png`, `04_student_home_mobile.png`

### 3.2 Curriculum Pathway (`/student/pathway`)
- **Action:** Learner explores the visual NCERT Class 8 concept graph.
- **Response:** Displays 30 concepts organized by chapter. Concepts with satisfied prerequisites show an "Unlocked" badge; unmastered prerequisites are locked with clear dependency indicators.
- **Evidence:** `screenshots/05_student_pathway_desktop.png`, `05_student_pathway_tablet.png`, `05_student_pathway_mobile.png`

### 3.3 Interactive Lesson Experience (`/student/lesson/:concept_id`)
- **Action:** Student selects "Read Lesson" for a concept (e.g., `MATH-C01` or `MATH-C04`).
- **Response:** Renders structured textbook content:
  1. *Key Principles:* Concise theoretical rules.
  2. *Worked Solutions:* Step-by-step algebraic derivations with mathematical notation.
  3. *Common Pitfalls:* Misconceptions to avoid.
  4. *Action:* "Take Diagnostic Assessment →"
- **Evidence:** `screenshots/06_student_lesson_desktop.png`, `06_student_lesson_tablet.png`, `06_student_lesson_mobile.png`

### 3.4 Diagnostic Assessment & Instant Authoritative Scoring (`/student/assessment/:concept_id`)
- **Action:** Student answers diagnostic questions (multiple-choice procedural and conceptual items).
  - Can optionally click "💡 Reveal Hint" to request tiered assistance.
  - Clicks "Submit & Evaluate Assessment".
- **Response:** 
  1. Frontend submits payload to `POST /api/v1/assessments/complete`.
  2. Backend scores authoritatively in < 20ms and commits to SQLite.
  3. Renders the **Assessment Results Canvas**:
     - Mastery Score Card (e.g., `3 / 3 • 100.0% • CONFIRM`).
     - Ready to Advance Badge & "Continue to Next Lesson →" CTA.
     - SUTRA AI Personalized Guidance Card.
     - Detailed Question-by-Question review with correct/incorrect markers and cognitive misconception pattern diagnosis.
- **Evidence:** `screenshots/07_student_assessment_desktop.png`, `07_student_assessment_tablet.png`, `07_student_assessment_mobile.png`

### 3.5 Student Progress & Attempt History (`/student/progress`)
- **Action:** Student views historical assessment attempts.
- **Response:** Displays tabular log of all completed assessments, scores, percentage, pass/fail status, and timestamp.
- **Evidence:** `screenshots/08_student_progress_desktop.png`, `08_student_progress_tablet.png`, `08_student_progress_mobile.png`

### 3.6 Spaced Retrieval & Memory Retention (`/student/insights`)
- **Action:** Student navigates to the Insights tab.
- **Response:** Displays the **Ebbinghaus Spaced Retrieval Queue**: concepts scheduled for reinforcement based on decay curves (1, 3, 7, 14 days), alerting students to review before forgetting occurs.

### 3.7 Grounded AI Tutor (`/student/tutor`)
- **Action:** Student converses with SUTRA AI on a specific concept.
  - Can switch between 6 Pedagogical Modes: *Guided Learning, Concept Explanation, Worked Examples, Diagnostic Practice, Check My Work, Prerequisite Support*.
- **Response:** Multi-turn dialogue with Socratic questioning. Responses nudge the student conceptually without exposing raw answers.
- **Evidence:** `screenshots/15_student_tutor_desktop.png`, `15_student_tutor_tablet.png`, `15_student_tutor_mobile.png`

---

## Stage 4: Educator Intelligence Workspace

### 4.1 Cohort Overview Dashboard (`/teacher/dashboard`)
- **Action:** Faculty views aggregate class progress.
- **Response:** Displays cohort size, average mastery score, active struggle alerts, distribution across mastery tiers, and recent student attempts.
- **Evidence:** `screenshots/09_teacher_dashboard_desktop.png`, `09_teacher_dashboard_tablet.png`, `09_teacher_dashboard_mobile.png`

### 4.2 Learner Directory (`/teacher/learners`)
- **Action:** Teacher filters and searches student roster.
- **Response:** Interactive table listing each student's active concept, overall mastery, last active timestamp, and quick-action links.
- **Evidence:** `screenshots/10_teacher_learners_desktop.png`, `10_teacher_learners_tablet.png`, `10_teacher_learners_mobile.png`

### 4.3 Individual Learner Audit Timeline (`/teacher/learners/:id`)
- **Action:** Teacher clicks on a specific student (e.g., Diya Patel).
- **Response:** Detailed diagnostic view displaying:
  - Mastery radar across all concepts.
  - Full attempt history with question-level breakdown.
  - Specific diagnosed cognitive misconceptions (e.g., `SIGN_ERROR`).
- **Evidence:** `screenshots/11_teacher_profile_desktop.png`, `11_teacher_profile_tablet.png`, `11_teacher_profile_mobile.png`

### 4.4 Curriculum Insights (`/teacher/insights`)
- **Action:** Teacher inspects concept-level difficulty across the cohort.
- **Response:** Identifies bottleneck concepts where pass rates are lowest and surfaces top recurring misconception tags.
- **Evidence:** `screenshots/12_teacher_insights_desktop.png`, `12_teacher_insights_tablet.png`, `12_teacher_insights_mobile.png`

### 4.5 Clinical Interventions & Mastery Overrides (`/teacher/interventions`)
- **Action:** Teacher selects a flagged student, adjusts their concept mastery (0–100%), and inputs a clinical rationale ($\ge 5$ characters).
- **Response:** Submits `POST /teacher/override`. Backend updates `student_concept_mastery`, recalculates prerequisite unlocks, and writes an immutable entry to `audit_logs`.
- **Evidence:** `screenshots/13_teacher_interventions_desktop.png`, `13_teacher_interventions_tablet.png`, `13_teacher_interventions_mobile.png`

### 4.6 Tamper-Evident Audit Log (`/teacher/audit`)
- **Action:** Teacher navigates to the audit ledger.
- **Response:** Displays chronological log of all administrative actions, clinical overrides, and security events, complete with Correlation IDs, actor IDs, and state diffs.
- **Evidence:** `screenshots/14_teacher_audit_desktop.png`, `14_teacher_audit_tablet.png`, `14_teacher_audit_mobile.png`

### 4.7 Educator AI Assistant (`/teacher/assistant`)
- **Action:** Teacher prompts the assistant: *"Which students require immediate scaffolding in linear equations?"*
- **Response:** Generates analysis strictly adhering to the **4-Level Evidence Hierarchy**:
  1. *Level 1 (Verified Database Facts):* Student IDs, actual attempt counts, and scores.
  2. *Level 2 (Calculated Statistics):* Pass rate percentages and averages.
  3. *Level 3 (Qualitative AI Interpretations):* Hypothesized cognitive root causes.
  4. *Level 4 (Recommended Actions):* Targeted pedagogical interventions.
- **Evidence:** `screenshots/16_teacher_assistant_desktop.png`, `16_teacher_assistant_tablet.png`, `16_teacher_assistant_mobile.png`

