# SUTRA LEARN — Database Architecture & Migration Specification
**Document ID:** `docs/14-database-and-migrations.md`  
**Execution Standard:** Database Architect + Data Integrity Engineer  
**Timestamp:** 2026-11-01T17:30:00+05:30  
**Status:** SCHEMA INITIALIZED, WAL ACTIVATED & INTEGRITY VERIFIED  

---

## 1. Storage Engine Topology & Concurrency Configuration

SUTRA LEARN persists data using an ACID-compliant SQLite 3 engine configured for high read concurrency, deterministic testing, and cloud persistence:

```sql
PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;
PRAGMA busy_timeout = 5000;
```

- **Write-Ahead Logging (WAL):** Writers append to the `-wal` log without blocking concurrent readers.
- **Busy Timeout:** 5000 ms timeout eliminates transient locking exceptions.
- **Foreign Key Enforcement:** Foreign keys are activated on every connection via `PRAGMA foreign_keys = ON;`.

---

## 2. Table Schemas & Relational Integrity

### 2.1 Table: `learners`
```sql
CREATE TABLE IF NOT EXISTS learners (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    grade INTEGER NOT NULL DEFAULT 8,
    role TEXT NOT NULL DEFAULT 'student', -- 'student' | 'teacher'
    password_hash TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 2.2 Table: `assessment_sessions`
```sql
CREATE TABLE IF NOT EXISTS assessment_sessions (
    id TEXT PRIMARY KEY,
    learner_id TEXT NOT NULL,
    concept_id TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'active', -- 'active' | 'completed'
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    FOREIGN KEY (learner_id) REFERENCES learners(id) ON DELETE CASCADE
);
```

### 2.3 Table: `attempts`
```sql
CREATE TABLE IF NOT EXISTS attempts (
    id TEXT PRIMARY KEY, -- Client-generated UUID for idempotency
    session_id TEXT,
    learner_id TEXT NOT NULL,
    question_id TEXT NOT NULL,
    concept_id TEXT NOT NULL,
    selected_option_id TEXT NOT NULL,
    is_correct INTEGER NOT NULL, -- 0 or 1
    hint_used INTEGER NOT NULL DEFAULT 0, -- 0 or 1
    misconception_tag TEXT DEFAULT 'none',
    cognitive_demand TEXT DEFAULT 'procedural',
    client_timestamp TIMESTAMP,
    server_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sync_status TEXT DEFAULT 'synced',
    FOREIGN KEY (learner_id) REFERENCES learners(id) ON DELETE CASCADE,
    FOREIGN KEY (session_id) REFERENCES assessment_sessions(id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_attempts_learner ON attempts(learner_id, concept_id);
```

### 2.4 Table: `concept_progress`
```sql
CREATE TABLE IF NOT EXISTS concept_progress (
    learner_id TEXT NOT NULL,
    concept_id TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'not_started', -- 'not_started' | 'in_progress' | 'needs_reinforcement' | 'mastered'
    unassisted_correct INTEGER NOT NULL DEFAULT 0,
    assisted_correct INTEGER NOT NULL DEFAULT 0,
    total_attempts INTEGER NOT NULL DEFAULT 0,
    mastery_percentage REAL NOT NULL DEFAULT 0.0,
    last_recommended_outcome TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (learner_id, concept_id),
    FOREIGN KEY (learner_id) REFERENCES learners(id) ON DELETE CASCADE
);
```

### 2.5 Table: `recommendations`
```sql
CREATE TABLE IF NOT EXISTS recommendations (
    id TEXT PRIMARY KEY,
    learner_id TEXT NOT NULL,
    concept_id TEXT NOT NULL,
    outcome TEXT NOT NULL, -- 'BRIDGE_BACK' | 'SCAFFOLD' | 'STRETCH' | 'CONFIRM' | 'TEACHER_REVIEW'
    target_concept_id TEXT NOT NULL,
    target_concept_title TEXT NOT NULL,
    target_activity_type TEXT NOT NULL,
    target_activity_id TEXT,
    reason_code TEXT NOT NULL,
    explanation TEXT NOT NULL,
    confidence_score REAL NOT NULL,
    evidence_summary_json TEXT NOT NULL,
    policy_version TEXT NOT NULL DEFAULT '1.0.0',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (learner_id) REFERENCES learners(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_recommendations_learner ON recommendations(learner_id, created_at);
```

### 2.6 Table: `teacher_overrides`
```sql
CREATE TABLE IF NOT EXISTS teacher_overrides (
    id TEXT PRIMARY KEY,
    learner_id TEXT NOT NULL,
    concept_id TEXT NOT NULL,
    previous_outcome TEXT NOT NULL,
    overridden_outcome TEXT NOT NULL,
    reason TEXT NOT NULL,
    teacher_id TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (learner_id) REFERENCES learners(id) ON DELETE CASCADE,
    FOREIGN KEY (teacher_id) REFERENCES learners(id) ON DELETE CASCADE
);
```

### 2.7 Table: `system_audit_logs`
```sql
CREATE TABLE IF NOT EXISTS system_audit_logs (
    id TEXT PRIMARY KEY,
    event_category TEXT NOT NULL, -- 'PEDAGOGICAL_INTERVENTIONS' | 'REJECTED_SECURITY_EVENTS' | 'SUCCESSFUL_AUTHORIZED_ACTIONS' | 'SYSTEM_EVENTS'
    actor_id TEXT NOT NULL,
    actor_role TEXT NOT NULL,
    learner_id TEXT,
    concept_id TEXT,
    previous_state TEXT,
    new_state TEXT,
    rationale TEXT,
    outcome TEXT NOT NULL, -- 'APPLIED' | 'REJECTED' | 'RECORDED'
    details TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_audit_category ON system_audit_logs(event_category, created_at);
```

### 2.8 Table: `ai_conversations` & `ai_messages`
```sql
CREATE TABLE IF NOT EXISTS ai_conversations (
    id TEXT PRIMARY KEY,
    owner_id TEXT NOT NULL,
    owner_role TEXT NOT NULL, -- 'student' | 'teacher'
    conversation_type TEXT NOT NULL DEFAULT 'tutor', -- 'tutor' | 'educator_assistant'
    title TEXT NOT NULL,
    concept_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES learners(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ai_messages (
    id TEXT PRIMARY KEY,
    conversation_id TEXT NOT NULL,
    sender_role TEXT NOT NULL, -- 'user' | 'assistant' | 'system'
    content TEXT NOT NULL,
    response_type TEXT DEFAULT 'standard',
    hints_json TEXT,
    concept_id TEXT,
    requires_follow_up INTEGER DEFAULT 0,
    provider_metadata TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES ai_conversations(id) ON DELETE CASCADE
);
```

---

## 3. Migration Guard & Non-Destructive Schema Evolution

In `backend/app/db/database.py`, `init_db()` executes migration guards:
- Checks column existence using `PRAGMA table_info(...)`.
- Applies non-destructive `ALTER TABLE` statements conditionally if columns are absent.
- Preserves existing student progress, attempts, and audit logs across all server boots.

