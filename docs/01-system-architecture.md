# SUTRA LEARN — System Architecture Specification
**Document ID:** `docs/01-system-architecture.md`  
**Execution Standard:** Principal Software Architect + Backend Architect  
**Timestamp:** 2026-11-01T17:29:00+05:30  
**Status:** CANONICAL ARCHITECTURE  

---

## 1. High-Level Architectural Topology

SUTRA LEARN is structured around clear separation of concerns across presentation, business services, database persistence, and multi-model AI routing:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        REACT FRONTEND (Vite / TS)                      │
│                                                                        │
│  [Unified Landing / Login] ──► Server Role Resolution                  │
│                                      │                                 │
│          ┌───────────────────────────┴───────────────────────────┐     │
│          ▼                                                       ▼     │
│  [Student Workspace]                                    [Educator Shell]
│  - Home                                                 - Dashboard    │
│  - Pathway (DAG)                                        - Learners     │
│  - Progress Dossier                                     - Dossier      │
│  - Learning Insights (/student/insights)                - Bottlenecks  │
│  - Contextual AI Tutor                                  - Interventions│
│  - Lesson & Assessment Runners                          - Assistant    │
│                                                         - Audit Trail  │
│  [IndexedDB Client Queue: pending_attempts & cached_content]           │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ HTTP / JSON (HMAC-SHA256 Bearer Token)
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        FASTAPI BACKEND SERVICE                         │
│                                                                        │
│  [Auth Router] ──► Token Verification & Database Role Resolution       │
│  [Metrics Service] ──► Single Source of Truth (56 Canonical Metrics)   │
│  [Adaptive Engine] ──► Deterministic Rule Policy (Scaffold/Bridge/...) │
│  [Math Validator] ──► Algebraic Evaluation & Distractor Diagnosis      │
│  [AI Router] ──► Multi-Model Provider Orchestrator                     │
│                  - Gemini (Cloud)                                      │
│                  - Ollama Qwen 3.5 4B / Gemma 4 E2B (Local Offline)    │
│                  - SUTRA Grounded Curriculum Fallback Engine           │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   SQLITE PERSISTENCE (WAL Mode)                        │
│                                                                        │
│  - learners                 - recommendations    - ai_conversations    │
│  - assessment_sessions      - teacher_overrides  - ai_messages         │
│  - attempts                 - system_audit_logs                        │
│  - concept_progress                                                    │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Core Architectural Invariants

1. **Single Source of Truth:** Metric values displayed in Student Home, Student Progress, Student Insights, and Educator Dossier originate from `app.services.metrics`. Zero frontend metric calculation drift.
2. **Authority Separation:** AI models provide conversational guidance and hints, but never write to mastery scores, attempt grades, or concept locks.
3. **Identity Verification:** Identity headers (`x-user-id`, `x-teacher-id`) are strictly rejected. Authentication is enforced via signed Bearer tokens verified against SQLite `learners.role`.
4. **Idempotent Attempt Processing:** Submissions carry client UUIDs. Duplicate submissions are recognized and acknowledged without inflating attempt counts or corrupting mastery statistics.
5. **Acyclic Concept DAG:** The NCERT Class 8 curriculum DAG (`MATH-C01` through `MATH-C06`) is formally acyclic, guaranteeing predictable traversal and prerequisite gap bridging.

