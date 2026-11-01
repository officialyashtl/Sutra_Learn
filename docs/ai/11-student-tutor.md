# SUTRA LEARN — AI ASCENSION 1000
## DOCUMENT 11: STUDENT TUTOR INTEGRATION & UX CONTRACT
**Version:** 1.0.0  
**Frontend Component:** `frontend/src/pages/StudentTutor.tsx`  
**Backend Endpoints:** `POST /api/v1/ai/tutor`, `POST /api/v1/tutor/chat`, `GET /api/v1/tutor/conversations`  
**Design Palette:** Earthbound Editorial (`#291C0E`, `#6E473B`, `#F8F5EF`, `#E1D4C2`)  

---

### 1. User Journey & Pedagogical Experience

The Student Tutor interface empowers students to ask open-ended questions about NCERT Class 8 algebra without the risk of AI homework hallucination.

```
+--------------------------------------------------------------------------+
|  SUTRA LEARN TUTOR          [ AI INFRASTRUCTURE STATUS: GEMMA 4 E2B ]   |
+--------------------------------------------------------------------------+
|                                                                          |
|  [Student]                                                               |
|  "I don't understand how to solve 2x + 5 = 15"                          |
|                                                                          |
|  [SUTRA Tutor]   [Gemma 4 E2B | Verified NCERT Grounding]                |
|  "Let's look at this together! Our goal is to isolate the term with x.   |
|   What operation would undo the +5 on the left-hand side?"              |
|                                                                          |
|  [Hint 1: Remember to do the exact same operation to both sides.]        |
|  [Hint 2: What is the inverse of addition?]                              |
|                                                                          |
+--------------------------------------------------------------------------+
|  [ Input Message...                                ] [ Send Question ]   |
+--------------------------------------------------------------------------+
```

---

### 2. Live Infrastructure Status Pill

At the header of `StudentTutor.tsx`, a persistent live status pill polls `GET /api/v1/ai/health`:
- If Gemini is active: Displays `GEMINI ACTIVE` (Golden Amber badge).
- If Qwen is active: Displays `QWEN 3.5 4B ACTIVE` (Olive Green badge).
- If Gemma is active: Displays `GEMMA 4 E2B ACTIVE` (Earth Terracotta badge).
- If Fallback is active: Displays `DETERMINISTIC FALLBACK` (Sand Slate badge).

---

### 3. Per-Message Provider Attribution Badge

Every assistant bubble displays:
- Provider display name (e.g., `Gemma 4 E2B (Local)` or `NCERT Curriculum Engine`).
- Mathematical validation status (`VERIFIED` or `CURRICULUM_VERIFIED`).
- Latency in milliseconds.
- Transparent fallback badge if remote services encountered errors.

---

### 4. Ownership & Privacy Security Guarantees

As verified in `test_tutor_conversation_ownership_isolation`:
- Conversations are partitioned by `learner_id`.
- Attempting to access conversation ID `conv_student_01` with `student-02` credentials returns HTTP 403 Forbidden.
- Message history is strictly encrypted in transit via JWT session claims.

