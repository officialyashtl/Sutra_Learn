# SUTRA LEARN PHOENIX 10,000
## DOCUMENT 13: EDUCATOR PORTAL & CLASSROOM INTELLIGENCE ASSISTANT
**Version:** 1.0.0  
**Domain 4 (500 pts) & Domain 13 (450 pts):** Authorization & Educator Experience  

---

### 1. Educator Portal Navigation

The Educator Portal (`frontend/src/components/EducatorShell.tsx`, `TeacherDashboard.tsx`, `TeacherLearners.tsx`, `TeacherInsights.tsx`, `TeacherInterventions.tsx`, `TeacherAudit.tsx`, `EducatorAssistant.tsx`) gives teachers clinical oversight over their classrooms:
- **Cohort Mastery Overview:** Real-time accuracy averages and risk indicators.
- **Learner Profiles:** Complete chronological attempt histories and concept mastery status.
- **Intervention Engine:** Manual teacher overrides with mandatory justification logging.
- **System Audit Trail:** Immutable record of all administrative actions.

---

### 2. Educator Assistant Integration

The Educator Assistant (`frontend/src/pages/EducatorAssistant.tsx`, `backend/app/routers/educator_assistant.py`, `backend/app/routers/ai.py`):
1. **Security Guard:** Strictly guarded by `require_teacher` dependency. If a student attempts to invoke `/api/v1/teacher/assistant/analyze` or `POST /api/v1/ai/educator`, FastAPI rejects the request with HTTP 403 Forbidden.
2. **Evidence-Grounded Analytics:**
   - Synthesizes real SQLite database records (`crud.get_teacher_cohort_summary()`).
   - Identifies struggling learners ($< 65\%$ accuracy).
   - Pinpoints bottleneck concepts with low unassisted mastery.
   - Recommends evidence-based differentiated instructional interventions.
3. **Structured Response Schema:** Returns verified facts separated from pedagogical advice, ensuring teachers understand the data basis for every recommendation.

