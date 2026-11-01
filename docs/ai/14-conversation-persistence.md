# SUTRA LEARN — AI ASCENSION 1000
## DOCUMENT 14: CONVERSATION PERSISTENCE & DATA SCHEMA
**Version:** 1.0.0  
**Storage Engine:** SQLite 3 with Write-Ahead Logging (`PRAGMA journal_mode=WAL;`)  
**Schema Definition:** `backend/app/db/database.py`  
**CRUD Module:** `backend/app/db/crud.py`  

---

### 1. Database Schema for AI Telemetry

AI interactions are persisted in two normalized relational tables:

```sql
CREATE TABLE IF NOT EXISTS ai_conversations (
    conversation_id TEXT PRIMARY KEY,
    owner_id TEXT NOT NULL,
    owner_role TEXT NOT NULL,
    title TEXT NOT NULL,
    conversation_type TEXT NOT NULL DEFAULT 'tutor',
    concept_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(owner_id) REFERENCES learners(learner_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ai_messages (
    message_id TEXT PRIMARY KEY,
    conversation_id TEXT NOT NULL,
    sender_role TEXT NOT NULL,
    content TEXT NOT NULL,
    response_type TEXT,
    hints TEXT,                -- Serialized JSON Array
    concept_id TEXT,
    requires_follow_up BOOLEAN DEFAULT 1,
    provider_metadata TEXT,    -- Serialized JSON Object (Provider, Model, Latency, Validation)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(conversation_id) REFERENCES ai_conversations(conversation_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_ai_conversations_owner ON ai_conversations(owner_id);
CREATE INDEX IF NOT EXISTS idx_ai_messages_conv ON ai_messages(conversation_id);
```

---

### 2. Provider Metadata Field Audit

Every assistant message stores full telemetry in `provider_metadata`:
```json
{
  "request_id": "req_ea717fdb9841",
  "provider": "NCERT Curriculum Engine",
  "model": "curriculum_fallback",
  "is_fallback": true,
  "fallback_reason": "Operating mode or provider availability routed to curriculum engine",
  "latency_ms": 19019.21,
  "validation_status": "CURRICULUM_VERIFIED"
}
```

---

### 3. Concurrency & WAL Integrity

- `PRAGMA journal_mode = WAL;`: Enables non-blocking concurrent readers while writing telemetry.
- `PRAGMA synchronous = NORMAL;`: Guarantees durability without crippling write performance.
- `PRAGMA foreign_keys = ON;`: Enforces referential integrity between conversations and learner records.

