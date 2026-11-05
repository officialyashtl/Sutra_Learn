# SUTRA LEARN — Judge Demonstration Scripts
### CodeKernel '26 Presentation & Evaluation Guide

This document provides three calibrated demonstration scripts tailored for live judging sessions, complete with exact navigation paths, timed narration, click-by-click instructions, and fallback procedures.

---

## 1. 3-Minute Concise Pitch (Fast Overview)

**Target Audience:** Product judges, general evaluators, time-constrained sessions.  
**Objective:** Prove the core problem, the dual-engine solution, live assessment scoring, and teacher visibility in under 180 seconds.

| Timestamp | Navigation / Screen | Action | Narration Script |
| :--- | :--- | :--- | :--- |
| **0:00 – 0:35** | `/` (Landing Page) | Open `https://sutralearn.vercel.app/` | "Judges, middle-school mathematics has a silent crisis: 70% of students struggle when transitioning to algebra, and current AI tools either hallucinate grades or spoon-feed answers that bypass learning. SUTRA LEARN solves this with a Dual-Engine architecture: deterministic mathematical scoring on the server, paired with a Socratic AI tutor. Let's see it live." |
| **0:35 – 1:30** | `/login` $\to$ `/student/home` $\to$ `/student/assessment/MATH-C01` | Log in as Aarav (`student-01`). Start quiz, answer 3 questions, click Submit. | "I'm logged in as Aarav. Notice this diagnostic assessment on Integer Arithmetic. When I submit, the grading does NOT go to an LLM. Our backend engine compares answers authoritatively in under 20 milliseconds. Look at this result: exact percentage, cognitive misconception diagnosis on incorrect options, and dynamic unlocking of the next lesson." |
| **1:30 – 2:15** | `/student/tutor` | Switch to SUTRA AI Tutor, select 'Guided Learning', ask: *"How do I solve 2x + 5 = 15?"* | "Now watch our SUTRA AI Tutor. Powered by Google Gemini, it doesn't give away $x = 5$. It uses Socratic questioning: 'What operation is currently being applied to the variable?' This guides the learner to discover the answer themselves." |
| **2:15 – 2:50** | `/teacher/login` $\to$ `/teacher/dashboard` | Log in as Ms. Ananya Roy (`teacher-01`). Show cohort heatmap and click 'Audit'. | "Finally, look at the teacher workspace. Teachers aren't locked out. Ms. Roy sees real-time struggle heatmaps across her entire cohort, can drill into individual student attempts, and can execute audited clinical overrides. Every action is cryptographically logged." |
| **2:50 – 3:00** | Conclusion | Pause on Dashboard | "SUTRA LEARN: Zero hallucination in grading, grounded Socratic tutoring, and complete educator authority. Fully deployed and ready for classroom adoption. Thank you." |

---

## 2. 5-Minute Standard Demonstration (Comprehensive)

**Target Audience:** General hackathon evaluation panels, product & UX specialists.  
**Objective:** Deliver an in-depth tour of the complete student learning loop, misconception diagnostics, spaced retrieval, and teacher interventions.

| Timestamp | Screen | Narrative & Operational Sequence |
| :--- | :--- | :--- |
| **0:00 – 1:00** | **The Problem & Brand Cover (`/`)** | Open Landing Page. Highlight the Earthbound Editorial aesthetic. Explain that middle school algebra concepts are interconnected in a Directed Acyclic Graph (DAG). Point out the unbreachable dual portal. |
| **1:00 – 2:15** | **Student Learning Loop (`/student/lesson` & `/assessment`)** | 1. Enter student workspace as Aarav (`student-01`).<br/>2. Open Lesson `MATH-C01` (Integer Arithmetic). Show worked steps and common pitfalls.<br/>3. Launch Assessment. Deliberately select one incorrect answer associated with a known misconception (e.g. sign error on subtraction).<br/>4. Submit quiz. Show instant (<20ms) server-side grading.<br/>5. Review the result: point out the green checkmarks, red crosses, the diagnosed misconception banner, and the "Continue to Next Lesson" unlock CTA. |
| **2:15 – 3:15** | **Grounded AI Tutor & Spaced Retrieval (`/student/tutor` & `/insights`)** | 1. Navigate to SUTRA AI Tutor.<br/>2. Show the 6 pedagogical modes (Guided Learning, Worked Example, Practice, Check My Work, Quick Revision, Prerequisites).<br/>3. Prompt: *"Why does the sign change when moving a term to the other side?"*<br/>4. Show Gemini Socratic explanation grounded in balance principles.<br/>5. Navigate to Insights tab: explain how the Ebbinghaus Spaced Retrieval Queue prevents forgetting through 1, 3, 7, 14-day intervals. |
| **3:15 – 4:30** | **Educator Intelligence & Clinical Override (`/teacher/*`)** | 1. Log out and enter `/teacher/login` as `teacher-01`.<br/>2. Cohort Dashboard: show struggle alert cards (identifying students failing prerequisites).<br/>3. Open Diya Patel's profile: show attempt history, hint usage, and recurring misconception tags.<br/>4. Demonstrate Clinical Override: adjust mastery score, type mandatory rationale (*"Demonstrated oral mastery during classroom whiteboard session"*), submit override.<br/>5. Navigate to Audit Log: show the immutable entry with correlation ID and state change diff. |
| **4:30 – 5:00** | **Architecture & Wrap-Up** | Present `docs/project_flowchart.svg`. Reiterate: 46/46 pytest tests passing, zero grading drift, production deployed on Vercel and Render. |

---

## 3. 7-Minute Technical Deep Dive (Engineering Evaluator)

**Target Audience:** Senior software architects, backend engineers, AI/ML evaluators, cybersecurity judges.  
**Objective:** Prove architectural integrity, server-authoritative scoring, decoupled Gemini resilience, SQLite WAL persistence, and security controls.

### 0:00 – 1:30: Dual-Engine Architecture & Separation of Concerns
- **Narration:** "Judges, the critical technical insight in SUTRA LEARN is strict separation of concerns. Large Language Models are brilliant at conceptual dialogue but fundamentally unsuited for authoritative grading due to temperature variance, prompt injection, and stochastic drift. In SUTRA LEARN, LLMs have 0% authority over scores, unlocks, or records."
- **Display:** Show `docs/PROJECT_FLOWCHART.md` and `docs/project_flowchart.svg`. Point out the boundary between the **Deterministic Adaptive Core** (FastAPI + SQLite) and the **Generative AI Layer** (Google Gemini).

### 1:30 – 3:00: Assessment Lifecycle, Scoring & Idempotency
- **Live Terminal / Network Tab:** Open Chrome DevTools Network Tab while submitting an assessment on `https://sutralearn.vercel.app`.
- **Key Points:**
  - `POST /api/v1/assessments/complete` finishes in **< 20 milliseconds**.
  - Payload carries client timestamp, session ID, and answer choices.
  - Backend performs authoritative comparison against `QUESTIONS_REGISTRY`.
  - Atomically commits attempt records, result summary, and prerequisite mastery updates in a single SQLite transaction with `PRAGMA journal_mode=WAL;`.
  - **Demonstrate Idempotency:** Double-click or replay the identical submission payload; backend returns the exact existing record ID without duplicating database rows.

### 3:00 – 4:30: Gemini Decoupling & Cloud Resilience
- **Narration:** "Notice that Gemini inference is decoupled from score persistence. When the student submits, the score and answers render immediately. The client then asynchronously requests deeper Socratic guidance via `POST /assessments/results/{id}/guidance`."
- **Surge Resilience Demonstration:** Explain how Google's Gemini API can encounter 503 high-demand surges. Show the multi-tier cascade in code:
  1. `gemini-flash-lite-latest`
  2. `gemini-3.1-flash-lite`
  3. `gemini-2.5-flash`
  4. Instant (<2ms) deterministic NCERT curriculum template fallback.
- **Evidence:** Point to `scripts/verify_rectification_matrix.py` where a live 503 cloud spike was absorbed with zero data loss.

### 4:30 – 5:45: Security, RBAC & Immutable Audit Trail
- **Live Demo:**
  - Show Bearer token decoding in DevTools (HMAC-SHA256 signature).
  - Demonstrate **Learner Isolation:** Show how student-02 attempting to fetch student-01's assessment result receives `HTTP 403 Forbidden`.
  - Demonstrate **Educator Intelligence Assistant (`/teacher/assistant`):** Show the 4-Level Evidence Hierarchy (Verified Facts $\to$ Statistics $\to$ AI Interpretation $\to$ Recommendations).
  - Open `/teacher/audit`: Show cryptographic correlation IDs tracing every pedagogical event.

### 5:45 – 7:00: Verification Evidence & Closing
- **Terminal Evidence:**
  - 46/46 pytest tests passing (100%).
  - 0 linter errors via `oxlint`.
  - Clean Vite build in 523ms.
- **Closing:** "SUTRA LEARN proves that generative AI in education only succeeds when bounded by deterministic mathematical truth. Thank you."

---

## 4. Fallback Demonstration Procedures

In the event of an external network failure, cloud rate-limiting, or host latency during a live presentation:

1. **If Render Backend Is Cold (Spin-Up Delay):**
   - *Symptom:* First API request takes 30–40 seconds to respond.
   - *Action:* While the backend wakes up, open `https://sutralearn.vercel.app/project_flowchart.svg` or explain the problem statement on the Landing Page.
   - *Narration:* "Our API is hosted on Render's free tier, which auto-spins down during inactivity. Notice how the frontend displays our SUTRA pulse loader rather than freezing or crashing."
2. **If Google Gemini API Returns 503 Surge:**
   - *Symptom:* AI Tutor displays fallback pedagogical hints.
   - *Action:* Point out that the system did NOT crash or fail.
   - *Narration:* "This is our multi-tier resilience in action. Because Google's free endpoint is experiencing a demand surge, SUTRA LEARN automatically engaged its local NCERT curriculum fallback within 2 milliseconds. The student continues learning without interruption."
3. **If Wi-Fi / Internet Disconnects Entirely:**
   - *Action:* Show the PWA offline capability.
   - *Narration:* "SUTRA LEARN is engineered with an offline Service Worker v2. The application shell remains loaded, and student attempts are safely queued in client-side IndexedDB until network restoration."

