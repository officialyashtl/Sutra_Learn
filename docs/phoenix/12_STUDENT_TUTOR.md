# SUTRA LEARN PHOENIX 10,000
## DOCUMENT 12: STUDENT LEARNING EXPERIENCE & TUTOR INTEGRATION
**Version:** 1.0.0  
**Domain 3 (650 pts) & Domain 12 (450 pts):** Frontend Engineering & Student Experience  

---

### 1. Student Portal Navigation & Layout Rhythm

The Student Portal (`frontend/src/pages/StudentHome.tsx`, `StudentPathway.tsx`, `StudentProgress.tsx`, `StudentTutor.tsx`) follows the Earthbound Editorial design standard:
- **Palette Tokens:** Espresso (`#291C0E`), Mocha (`#6E473B`), Linen (`#E1D4C2`), Paper (`#F8F5EF`), Warm Surface (`#F2ECE3`).
- **Typography:** Serif editorial headers paired with clean monospace/sans mathematical formula presentation.
- **Rhythm:** Restrained margins, generous whitespace, structured cards with subtle border contrasts (`border-stone/30`).

---

### 2. Student AI Tutor Interface

The Tutor view (`frontend/src/pages/StudentTutor.tsx`) provides:
1. **Live Infrastructure Status Pill:**
   - Displays real-time operational provider state (`GEMINI ACTIVE`, `QWEN 3.5 4B ACTIVE`, `GEMMA 4 E2B ACTIVE`, `DETERMINISTIC FALLBACK`).
   - Driven by polling `GET /api/v1/ai/health`.
2. **Per-Message Attribution Badges:**
   - Explicitly displays the provider name (e.g. `Gemma 4 E2B (Local)` or `NCERT Curriculum Engine`), latency, and mathematical validation status.
3. **Progressive Hint Scaffolding:**
   - Renders expandable hint chips without spoiling the answer.
4. **Teaching Mode Selector:**
   - `guided_learning`: Socratic questioning.
   - `worked_example`: Step-by-step NCERT demonstration.
   - `practice`: Formative concept quiz.

---

### 3. Object-Level Tenant Privacy

Verified by automated testing (`test_tutor_conversation_ownership_isolation` and Stage 12 of `verify_e2e.py`):
- Student conversations are partitioned by `owner_id`.
- Attempting to access Student A's conversation ID with Student B's token returns HTTP 403 Forbidden.

