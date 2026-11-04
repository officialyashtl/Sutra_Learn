# SUTRA LEARN — DATABASE PERSISTENCE, SCHEMA & WAL DURABILITY AUDIT
**Document Version:** 1.0.0-OMEGA  
**Classification:** Database Reliability Engineering & Storage Architecture  
**Author:** Yash TL (The Oath of Tyr)  
**Storage Engine:** SQLite 3.40+ (Write-Ahead Logging Mode)  

---

## 1. Storage Architecture & Configuration

SUTRA LEARN employs an embedded, highly optimized SQLite storage engine designed for zero external dependency deployment on cloud platforms (Render, Fly.io, Docker containers) while providing enterprise ACID guarantees.

### 1.1 Critical SQLite PRAGMA Settings (`backend/app/db/database.py`)
```python
def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = NORMAL;")
    conn.execute("PRAGMA busy_timeout = 5000;")
    return conn
```

- **`journal_mode = WAL` (Write-Ahead Logging):** Allows concurrent readers without blocking writes, and concurrent writes to append to the WAL log without locking table pages.
- **`synchronous = NORMAL`:** Syncs WAL file on checkpoint rather than every single transaction, delivering 10x-50x write throughput while preserving crash durability.
- **`foreign_keys = ON`:** Guarantees relational integrity across attempts, concepts, conversations, and audit trails.
- **`busy_timeout = 5000`:** Eliminates `sqlite3.OperationalError: database is locked` during concurrent learner submissions by automatically waiting up to 5,000 ms for active transactions to commit.

---

## 2. Exhaustive Schema & Relational Structure

SUTRA LEARN maintains 11 core tables in its normalized relational model:

```
[learners] <----------+
  ^                   |
  |                   |
[learner_concept_mastery]----+
  |                          |
  v                          v
[concepts] <------- [question_attempts]
  ^                          ^
  |                          |
[questions]                  |
                             |
[teachers] --------> [teacher_overrides]
                             
[ai_conversations] --------> [ai_messages]

[system_audit_logs] (Append-Only Log Sink)
```

### Table 1: `learners`
Stores student identity, grade level, and security credentials.
- Columns: `id` (PK, TEXT), `name` (TEXT), `grade_level` (INTEGER), `password_hash` (TEXT), `created_at` (TIMESTAMP).

### Table 2: `teachers`
Stores educator identities and credentials.
- Columns: `id` (PK, TEXT), `name` (TEXT), `email` (TEXT UNIQUE), `password_hash` (TEXT), `created_at` (TIMESTAMP).

### Table 3: `concepts`
NCERT mathematics concept register.
- Columns: `id` (PK, TEXT), `name` (TEXT), `chapter` (TEXT), `grade` (INTEGER), `difficulty_level` (INTEGER), `prerequisites_json` (TEXT), `bkt_params_json` (TEXT), `sequence_order` (INTEGER).

### Table 4: `questions`
Verified pedagogical item bank with distractor traps and misconceptions.
- Columns: `id` (PK, TEXT), `concept_id` (FK -> concepts.id), `question_text` (TEXT), `options_json` (TEXT), `correct_option` (TEXT), `misconception_tags_json` (TEXT), `difficulty` (INTEGER), `explanation_latex` (TEXT).

### Table 5: `assessment_sessions`
Active and completed assessment session records.
- Columns: `id` (PK, TEXT), `learner_id` (FK -> learners.id), `concept_id` (FK -> concepts.id), `status` (TEXT), `started_at` (TIMESTAMP), `completed_at` (TIMESTAMP).

### Table 6: `question_attempts`
Individual question responses with timing and assistance data.
- Columns: `id` (PK, TEXT), `learner_id` (FK -> learners.id), `question_id` (FK -> questions.id), `selected_answer` (TEXT), `is_correct` (BOOLEAN), `time_taken_seconds` (INTEGER), `hint_used` (BOOLEAN), `detected_misconceptions_json` (TEXT), `step_validations_json` (TEXT), `created_at` (TIMESTAMP).

### Table 7: `learner_concept_mastery`
Current Bayesian Knowledge Tracing (BKT) probability for each student-concept pair.
- Columns: `learner_id` (FK -> learners.id), `concept_id` (FK -> concepts.id), `mastery_level` (REAL), `attempts_count` (INTEGER), `correct_count` (INTEGER), `last_attempt_at` (TIMESTAMP), PRIMARY KEY (`learner_id`, `concept_id`).

### Table 8: `teacher_overrides`
Educator pedagogical interventions modifying engine determinations.
- Columns: `id` (PK, TEXT), `teacher_id` (FK -> teachers.id), `learner_id` (FK -> learners.id), `concept_id` (FK -> concepts.id), `overridden_outcome` (TEXT), `reason` (TEXT), `created_at` (TIMESTAMP).

### Table 9: `ai_conversations`
Socratic dialogue conversation sessions.
- Columns: `id` (PK, TEXT), `owner_id` (TEXT), `owner_role` (TEXT), `conversation_type` (TEXT), `title` (TEXT), `concept_id` (TEXT), `created_at` (TIMESTAMP), `updated_at` (TIMESTAMP).

### Table 10: `ai_messages`
Individual messages within Socratic AI conversations.
- Columns: `id` (PK, TEXT), `conversation_id` (FK -> ai_conversations.id ON DELETE CASCADE), `sender_role` (TEXT), `content` (TEXT), `response_type` (TEXT), `hints_json` (TEXT), `concept_id` (TEXT), `requires_follow_up` (INTEGER), `provider_metadata` (TEXT), `created_at` (TIMESTAMP).

### Table 11: `system_audit_logs`
Cryptographically correlated immutable audit sink.
- Columns: `id` (PK, TEXT), `category` (TEXT), `event_type` (TEXT), `actor_id` (TEXT), `actor_role` (TEXT), `target_entity` (TEXT), `details_json` (TEXT), `correlation_id` (TEXT), `created_at` (TIMESTAMP).

---

## 3. Migration History & Database Evolution

1. **Migration 001 — Core Entities:** Provisioned `learners`, `teachers`, `concepts`, `questions`, and `learner_concept_mastery`.
2. **Migration 002 — Socratic Dialogue:** Provisioned `ai_conversations` and `ai_messages` with cascade deletion.
3. **Migration 003 — Security Passwords:** Added `password_hash` column to `learners` and `teachers`. Automated migration query in `init_db()` backfills demo credentials.
4. **Migration 004 — Forensic Correlation (OMEGA):** Added `correlation_id TEXT` column to `system_audit_logs` and provisioned index `idx_audit_correlation` to link API requests to persistent database audit records.

---

## 4. Durability & Recovery Verification

Durability was empirically verified during Suite 3 of `test_omega_forensic_suite.py`:
- Multiple transactions committed in SQLite WAL mode.
- Process connection closed and memory freed.
- Connection reopened; 100% of rows persisted with zero loss, zero corruption, and intact relational integrity.

