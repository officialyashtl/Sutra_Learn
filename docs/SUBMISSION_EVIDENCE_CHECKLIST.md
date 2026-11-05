# SUTRA LEARN — Submission Evidence Checklist
### CodeKernel '26 Evidence Inventory & Asset Matrix

This checklist inventories every verifiable piece of evidence supporting the **SUTRA LEARN** submission, linking directly to local repository assets, screenshot captures, and hosted production endpoints.

---

## 1. Visual Interface Screenshots (48 Verified Captures)

All screenshots are stored locally in `screenshots/` and captured across three viewports: **Desktop** ($1440\times960$), **Tablet** ($1024\times768$), and **Mobile** ($390\times844$).

| Screen # | Module / View | Desktop File | Tablet File | Mobile File | Status |
| :---: | :--- | :--- | :--- | :--- | :---: |
| 01 | Portal Gateway (Public Cover) | `screenshots/01_root_gateway_desktop.png` | `01_root_gateway_tablet.png` | `01_root_gateway_mobile.png` | **VERIFIED** |
| 02 | Student Login Gateway | `screenshots/02_student_login_desktop.png` | `02_student_login_tablet.png` | `02_student_login_mobile.png` | **VERIFIED** |
| 03 | Teacher Login Gateway | `screenshots/03_teacher_login_desktop.png` | `03_teacher_login_tablet.png` | `03_teacher_login_mobile.png` | **VERIFIED** |
| 04 | Student Learning Hub | `screenshots/04_student_home_desktop.png` | `04_student_home_tablet.png` | `04_student_home_mobile.png` | **VERIFIED** |
| 05 | NCERT Curriculum Pathway | `screenshots/05_student_pathway_desktop.png` | `05_student_pathway_tablet.png` | `05_student_pathway_mobile.png` | **VERIFIED** |
| 06 | Structured Lesson View | `screenshots/06_student_lesson_desktop.png` | `06_student_lesson_tablet.png` | `06_student_lesson_mobile.png` | **VERIFIED** |
| 07 | Diagnostic Assessment & Review | `screenshots/07_student_assessment_desktop.png` | `07_student_assessment_tablet.png` | `07_student_assessment_mobile.png` | **VERIFIED** |
| 08 | Student Historical Progress | `screenshots/08_student_progress_desktop.png` | `08_student_progress_tablet.png` | `08_student_progress_mobile.png` | **VERIFIED** |
| 09 | Teacher Cohort Dashboard | `screenshots/09_teacher_dashboard_desktop.png` | `09_teacher_dashboard_tablet.png` | `09_teacher_dashboard_mobile.png` | **VERIFIED** |
| 10 | Teacher Learner Roster | `screenshots/10_teacher_learners_desktop.png` | `10_teacher_learners_tablet.png` | `10_teacher_learners_mobile.png` | **VERIFIED** |
| 11 | Individual Learner Profile | `screenshots/11_teacher_profile_desktop.png` | `11_teacher_profile_tablet.png` | `11_teacher_profile_mobile.png` | **VERIFIED** |
| 12 | Curriculum Insights | `screenshots/12_teacher_insights_desktop.png` | `12_teacher_insights_tablet.png` | `12_teacher_insights_mobile.png` | **VERIFIED** |
| 13 | Clinical Interventions & Overrides | `screenshots/13_teacher_interventions_desktop.png` | `13_teacher_interventions_tablet.png` | `13_teacher_interventions_mobile.png` | **VERIFIED** |
| 14 | Immutable Audit Log Ledger | `screenshots/14_teacher_audit_desktop.png` | `14_teacher_audit_tablet.png` | `14_teacher_audit_mobile.png` | **VERIFIED** |
| 15 | SUTRA Grounded AI Tutor | `screenshots/15_student_tutor_desktop.png` | `15_student_tutor_tablet.png` | `15_student_tutor_mobile.png` | **VERIFIED** |
| 16 | Educator AI Assistant | `screenshots/16_teacher_assistant_desktop.png` | `16_teacher_assistant_tablet.png` | `16_teacher_assistant_mobile.png` | **VERIFIED** |

---

## 2. Architectural Diagrams & Vector Graphics

| Asset Description | File Path | Format / Size | Status |
| :--- | :--- | :--- | :---: |
| End-to-End Architectural Flowchart | [`docs/project_flowchart.svg`](project_flowchart.svg) | Clean Vector SVG (22,217 bytes) | **VERIFIED** |
| Public Static Flowchart | [`frontend/public/project_flowchart.svg`](../frontend/public/project_flowchart.svg) | Clean Vector SVG (22,217 bytes) | **VERIFIED** |
| System Architecture Specification | [`docs/SYSTEM_ARCHITECTURE.md`](SYSTEM_ARCHITECTURE.md) | Markdown with Mermaid diagrams | **VERIFIED** |
| High-Level Flowchart Documentation | [`docs/PROJECT_FLOWCHART.md`](PROJECT_FLOWCHART.md) | Markdown with ASCII/Mermaid | **VERIFIED** |

---

## 3. Automated Verification Evidence

| Evidence Type | Execution Command | Output File / Record | Verification Result |
| :--- | :--- | :--- | :---: |
| Full Backend Test Suite | `python -m pytest backend/tests/` | Console output & Pytest Runner | **46 / 46 Passing (100%)** |
| Rectification Matrix Suite | `python scripts/verify_rectification_matrix.py` | `scripts/verify_rectification_matrix.py` | **10 / 10 Passing (100%)** |
| Frontend Oxlint Analysis | `npm --prefix frontend run lint` | Console output | **0 Errors, 0 Warnings** |
| Production Frontend Build | `npm --prefix frontend run build` | `frontend/dist/` bundle (Vite v8.3.5) | **Built clean in 523ms** |
| Production Health Check | `GET /api/v1/health` | Live HTTP response | **HTTP 200 (database_mode: wal)** |
| Public Robots.txt Directives | `GET /robots.txt` | Live HTTP response | **HTTP 200 (447 bytes)** |
| Public Sitemap Directives | `GET /sitemap.xml` | Live HTTP response | **HTTP 200 (668 bytes)** |

---

## 4. Code & Configuration Reference Evidence

| Claim | Verified Code Source | Line Reference |
| :--- | :--- | :--- |
| Zero LLM Grading | [`backend/app/routers/assessment.py`](../backend/app/routers/assessment.py) | Lines 295–350: Direct comparison against `QUESTIONS_REGISTRY` |
| Options Array Serialization | [`backend/app/schemas.py`](../backend/app/schemas.py) | Line 121: `options: List[Dict[str, Any]] = Field(...)` |
| Decoupled Gemini Guidance | [`backend/app/routers/assessment.py`](../backend/app/routers/assessment.py) | Lines 450–495: Result committed to SQLite before guidance |
| Multi-Path Result Retriever | [`backend/app/routers/assessment.py`](../backend/app/routers/assessment.py) | Lines 530–575: `get_assessment_result_unified` |
| UI Fault Isolation Shield | [`frontend/src/components/ErrorBoundary.tsx`](../frontend/src/components/ErrorBoundary.tsx) | Lines 15–70: `<ErrorBoundary>` component |
| Service Worker v2 Response Guarantee | [`frontend/public/sw.js`](../frontend/public/sw.js) | Lines 45–80: Valid `new Response(...)` resolution |
| 4-Level Evidence Hierarchy | [`frontend/src/pages/EducatorAssistant.tsx`](../frontend/src/pages/EducatorAssistant.tsx) | Lines 307–340: Structured evidence rendering |

---

## 5. Missing Evidence & Disclosed Gaps

- **Audio/Video Screencast:** A live screencast `.mp4` file is not currently hosted inside the Git repository (to prevent repo bloat > 100MB). Live judges should refer to the interactive walkthrough at `https://sutralearn.vercel.app/` or run the local demo scripts in `docs/DEMO_SCRIPT.md`.
- **Render Cold-Boot Evidence:** First connection to `https://sutra-learn-api.onrender.com` may take 30–50s due to free-tier hibernation. Subsequent connections respond in < 80ms.

