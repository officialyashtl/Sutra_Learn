# SUTRA LEARN — AI ASCENSION 1000
## DOCUMENT 12: EDUCATOR ASSISTANT INTEGRATION & ANALYTICS SPECIFICATION
**Version:** 1.0.0  
**Frontend Component:** `frontend/src/pages/EducatorAssistant.tsx`  
**Backend Endpoints:** `POST /api/v1/ai/educator`, `POST /api/v1/teacher/assistant/analyze`  
**Security Guard:** `require_teacher` dependency (HTTP 403 Forbidden on Student tokens)  

---

### 1. Pedagogical Mission

The Educator Assistant synthesizes student performance data into actionable teaching insights. Rather than forcing teachers to parse raw telemetry logs, the system converts attempt logs into diagnostic dossiers.

---

### 2. Evidence Grounding & Database Contract

The assistant queries live SQLite tables to guarantee zero-hallucination insights:
1. `crud.get_teacher_cohort_summary(conn)`: Returns student name, attempts, accuracy percentage, and review flags.
2. `crud.get_teacher_concept_analytics(conn)`: Returns unassisted accuracy per concept and dominant misconception distractor frequencies.

---

### 3. Structured Educator Output Schema

Every analysis yields an `AIEducatorResponse`:
```json
{
  "conversation_id": "conv_t_8f3a9e2d1c",
  "message_id": "msg_4b1a7d8c9e",
  "summary": "**Classroom Diagnostic Synthesis**\n\n**Verified Database Facts:**\n- Cohort comprises 4 registered learners in Class 8 Mathematics.\n- 1 learner(s) currently flag cognitive friction...",
  "observations": [
    "Cohort comprises 4 registered learners in Class 8 Mathematics.",
    "1 learner(s) currently flag cognitive friction or have an accuracy rate below 65%."
  ],
  "recommended_actions": [
    "Conduct a targeted 10-minute small-group review on negative signs and inverse operation sequencing.",
    "Use the SUTRA clinical intervention workflow to assign scaffolded practice before advancing learners to multi-step distribution problems."
  ],
  "struggling_learner_count": 1,
  "low_accuracy_concepts": ["MATH-C01"],
  "provider_metadata": {
    "provider": "SutraEducatorIntelligenceEngine",
    "model": "ncert-class8-analytics-v1",
    "is_fallback": false
  }
}
```

---

### 4. Role Authorization Invariant

Verified in `Stage 13` of `verify_e2e.py` and unit test `test_educator_intelligence_security_and_synthesis`:
- If a caller with `role="student"` submits a request to `/api/v1/ai/educator` or `/api/v1/teacher/assistant/analyze`, FastAPI immediately rejects the call with HTTP 403 Forbidden.
- Only tokens bearing `role="teacher"` or `role="admin"` can access classroom diagnostics.

