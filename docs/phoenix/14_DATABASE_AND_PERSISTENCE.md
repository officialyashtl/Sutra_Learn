# SUTRA LEARN PHOENIX 10,000
## DOCUMENT 14: DATABASE SCHEMA & CONVERSATION PERSISTENCE
**Version:** 1.0.0  
**Domain 5 (450 pts):** Database Integrity & Persistence  

---

### 1. SQLite Relational Schema

The persistence layer (`backend/app/db/database.py`) operates in Write-Ahead Logging (`WAL`) mode with foreign key validation enforced on every connection:

```sql
PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;
PRAGMA synchronous = NORMAL;
```

#### Core Database Tables:
1. `learners`: Stores learner and teacher profiles, roles (`student`, `teacher`, `admin`), and creation timestamps.
2. `concepts`: Stores NCERT concepts (`MATH-C01` to `MATH-C06`), descriptions, and prerequisite foreign keys.
3. `questions`: Question bank with stems, options, correct answers, and misconception distractor mapping.
4. `attempts`: Records learner assessment answers, timestamps, accuracy booleans, and hint usage.
5. `concept_progress`: Tracks mastery state, consecutive correct answers, and assigned learning pathway.
6. `teacher_overrides`: Records clinical teacher interventions with required justification strings.
7. `ai_conversations`: Stores conversational threads partitioned by `owner_id`.
8. `ai_messages`: Stores structured AI messages, hints, telemetry, and validation statuses.
9. `system_audit_logs`: Immutable audit trail of administrative events.

---

### 2. Indexes & Performance Optimization

```sql
CREATE INDEX IF NOT EXISTS idx_attempts_learner ON attempts(learner_id);
CREATE INDEX IF NOT EXISTS idx_attempts_concept ON attempts(concept_id);
CREATE INDEX IF NOT EXISTS idx_concept_progress_learner ON concept_progress(learner_id);
CREATE INDEX IF NOT EXISTS idx_ai_conversations_owner ON ai_conversations(owner_id);
CREATE INDEX IF NOT EXISTS idx_ai_messages_conv ON ai_messages(conversation_id);
```

---

### 3. Concurrency & WAL Mode Verification

Verified in Stage 01 of `verify_e2e.py`:
- `GET /api/v1/health` reports `database_mode = "wal"`.
- Enables non-blocking concurrent readers while background threads persist telemetry.
- Zero foreign key violations verified via `PRAGMA foreign_key_check;`.

