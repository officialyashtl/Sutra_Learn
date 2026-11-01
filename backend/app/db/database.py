"""
SUTRA LEARN - SQLite Database Connection & Schema Migration
Enforces WAL mode, foreign key constraints, connection pooling, and schema initialization.
"""

import os
import sqlite3
from pathlib import Path

def get_db_path() -> str:
    return os.environ.get(
        "SUTRA_DB_PATH",
        str(Path(__file__).resolve().parent.parent.parent / "sutra_learn.db")
    )


def get_db_connection() -> sqlite3.Connection:
    """
    Returns a configured SQLite connection with foreign keys enabled and Row factory.
    """
    conn = sqlite3.connect(get_db_path(), timeout=10.0, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS learners (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    grade INTEGER NOT NULL DEFAULT 8,
    role TEXT NOT NULL DEFAULT 'student', -- 'student' | 'teacher'
    password_hash TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS assessment_sessions (
    id TEXT PRIMARY KEY,
    learner_id TEXT NOT NULL,
    concept_id TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'active', -- 'active' | 'completed'
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    FOREIGN KEY (learner_id) REFERENCES learners(id) ON DELETE CASCADE
);

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

CREATE TABLE IF NOT EXISTS concept_progress (
    learner_id TEXT NOT NULL,
    concept_id TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'not_started', -- 'not_started' | 'in_progress' | 'needs_reinforcement' | 'mastered'
    unassisted_correct INTEGER NOT NULL DEFAULT 0,
    assisted_correct INTEGER NOT NULL DEFAULT 0,
    total_attempts INTEGER NOT NULL DEFAULT 0,
    mastery_percentage REAL DEFAULT 0.0,
    last_recommended_outcome TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (learner_id, concept_id),
    FOREIGN KEY (learner_id) REFERENCES learners(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS recommendations (
    id TEXT PRIMARY KEY,
    learner_id TEXT NOT NULL,
    concept_id TEXT NOT NULL,
    outcome TEXT NOT NULL,
    target_concept_id TEXT NOT NULL,
    target_concept_title TEXT NOT NULL,
    target_activity_type TEXT NOT NULL,
    target_activity_id TEXT,
    reason_code TEXT NOT NULL,
    explanation TEXT NOT NULL,
    confidence_score REAL NOT NULL,
    evidence_summary_json TEXT NOT NULL,
    policy_version TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (learner_id) REFERENCES learners(id) ON DELETE CASCADE
);

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
    FOREIGN KEY (teacher_id) REFERENCES learners(id)
);

CREATE TABLE IF NOT EXISTS system_audit_logs (
    id TEXT PRIMARY KEY,
    event_category TEXT NOT NULL, -- 'PEDAGOGICAL_INTERVENTIONS' | 'REJECTED_SECURITY_EVENTS' | 'SUCCESSFUL_AUTHORIZED_ACTIONS' | 'SYSTEM_EVENTS'
    actor_id TEXT NOT NULL,
    actor_role TEXT,
    learner_id TEXT,
    concept_id TEXT,
    previous_state TEXT,
    new_state TEXT,
    rationale TEXT,
    outcome TEXT NOT NULL, -- 'APPLIED' | 'REJECTED' | 'RECORDED'
    details TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

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

CREATE INDEX IF NOT EXISTS idx_ai_conversations_owner ON ai_conversations(owner_id, conversation_type);

CREATE TABLE IF NOT EXISTS ai_messages (
    id TEXT PRIMARY KEY,
    conversation_id TEXT NOT NULL,
    sender_role TEXT NOT NULL, -- 'user' | 'assistant' | 'system'
    content TEXT NOT NULL,
    response_type TEXT DEFAULT 'standard', -- 'guided_explanation' | 'worked_example' | 'hint' | 'practice_question' | 'check_work' | 'educator_summary' | 'educator_intervention'
    hints_json TEXT, -- Optional JSON array of progressive hints
    concept_id TEXT,
    requires_follow_up INTEGER DEFAULT 0,
    provider_metadata TEXT, -- JSON metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES ai_conversations(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_ai_messages_conv ON ai_messages(conversation_id, created_at);
"""


def init_db(db_path: str = None):
    """Initializes tables and seeds default learner and teacher profiles if empty."""
    target_path = db_path or get_db_path()
    conn = sqlite3.connect(target_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.executescript(SCHEMA_SQL)

    # Migration guard: Ensure password_hash column exists
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(learners);")
    columns = [row[1] for row in cursor.fetchall()]
    if "password_hash" not in columns:
        cursor.execute("ALTER TABLE learners ADD COLUMN password_hash TEXT;")
        conn.commit()

    # Import hash helper
    from app.auth import hash_password

    # Seed demo users if not present
    cursor.execute("SELECT COUNT(*) FROM learners;")
    count = cursor.fetchone()[0]
    if count == 0:
        student_pw = hash_password("sutra123")
        teacher_pw = hash_password("teacher123")

        cursor.execute(
            "INSERT INTO learners (id, name, grade, role, password_hash) VALUES (?, ?, ?, ?, ?);",
            ("student-01", "Aarav Sharma", 8, "student", student_pw)
        )
        cursor.execute(
            "INSERT INTO learners (id, name, grade, role, password_hash) VALUES (?, ?, ?, ?, ?);",
            ("student-02", "Diya Patel", 8, "student", student_pw)
        )
        cursor.execute(
            "INSERT INTO learners (id, name, grade, role, password_hash) VALUES (?, ?, ?, ?, ?);",
            ("student-03", "Kabir Sen", 8, "student", student_pw)
        )
        cursor.execute(
            "INSERT INTO learners (id, name, grade, role, password_hash) VALUES (?, ?, ?, ?, ?);",
            ("teacher-01", "Ms. Ananya Roy", 8, "teacher", teacher_pw)
        )
        conn.commit()
    conn.close()
