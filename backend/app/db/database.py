"""
SUTRA LEARN - SQLite Database Connection & Schema Migration
Enforces WAL mode, foreign key constraints, connection pooling, and schema initialization.
"""

import os
import sqlite3
from pathlib import Path

def get_db_path() -> str:
    env_path = os.environ.get("SUTRA_DB_PATH")
    if env_path:
        if os.path.isabs(env_path) and os.path.exists(env_path):
            return env_path
        if os.path.exists(env_path) and os.path.getsize(env_path) > 0:
            return env_path
        # Check relative to backend directory
        backend_rel = Path(__file__).resolve().parent.parent.parent / env_path
        if backend_rel.exists() and backend_rel.stat().st_size > 0:
            return str(backend_rel)
    # Canonical absolute fallback: backend/sutra_learn.db
    return str(Path(__file__).resolve().parent.parent.parent / "sutra_learn.db")


def get_db_connection() -> sqlite3.Connection:
    """
    Returns a configured SQLite connection with foreign keys enabled, WAL-friendly busy timeout, and Row factory.
    """
    conn = sqlite3.connect(get_db_path(), timeout=10.0, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA busy_timeout = 10000;")
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

CREATE TABLE IF NOT EXISTS assessment_results (
    id TEXT PRIMARY KEY,
    session_id TEXT,
    learner_id TEXT NOT NULL,
    concept_id TEXT NOT NULL,
    score INTEGER NOT NULL,
    total_questions INTEGER NOT NULL,
    percentage REAL NOT NULL,
    passed INTEGER NOT NULL DEFAULT 1,
    outcome TEXT NOT NULL,
    next_concept_id TEXT,
    next_concept_title TEXT,
    can_advance INTEGER NOT NULL DEFAULT 1,
    questions_detail_json TEXT NOT NULL,
    misconceptions_json TEXT,
    ai_guidance_json TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (learner_id) REFERENCES learners(id) ON DELETE CASCADE,
    FOREIGN KEY (session_id) REFERENCES assessment_sessions(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_assessment_results_learner_concept ON assessment_results(learner_id, concept_id, created_at);

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
    correlation_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_audit_category ON system_audit_logs(event_category, created_at);

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

CREATE TABLE IF NOT EXISTS spaced_retrieval_records (
    learner_id TEXT NOT NULL,
    concept_id TEXT NOT NULL,
    stability_days REAL NOT NULL DEFAULT 1.5,
    ease_factor REAL NOT NULL DEFAULT 2.5,
    repetitions INTEGER NOT NULL DEFAULT 0,
    last_practiced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estimated_retention REAL NOT NULL DEFAULT 1.0,
    next_review_due TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    retrieval_status TEXT NOT NULL DEFAULT 'CONSOLIDATED',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (learner_id, concept_id),
    FOREIGN KEY (learner_id) REFERENCES learners(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_spaced_retrieval_due ON spaced_retrieval_records(learner_id, next_review_due);
"""


def init_db(db_path: str = None):
    """Initializes tables and seeds default learner and teacher profiles if empty."""
    target_path = db_path or get_db_path()
    conn = sqlite3.connect(target_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA busy_timeout = 10000;")
    conn.executescript(SCHEMA_SQL)

    # Migration guard: Ensure password_hash column exists
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(learners);")
    columns = [row[1] for row in cursor.fetchall()]
    if "password_hash" not in columns:
        cursor.execute("ALTER TABLE learners ADD COLUMN password_hash TEXT;")
        conn.commit()

    # Migration guard: Ensure correlation_id column exists on system_audit_logs
    cursor.execute("PRAGMA table_info(system_audit_logs);")
    audit_cols = [row[1] for row in cursor.fetchall()]
    if "correlation_id" not in audit_cols:
        cursor.execute("ALTER TABLE system_audit_logs ADD COLUMN correlation_id TEXT;")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_audit_correlation ON system_audit_logs(correlation_id);")
        conn.commit()

    # Import hash helper
    from app.auth import hash_password

    # Seed demo users if not present
    cursor.execute("SELECT COUNT(*) FROM learners;")
    count = cursor.fetchone()[0]
    student_pw = hash_password("sutra123")
    teacher_pw = hash_password("teacher123")

    if count == 0:
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
    else:
        # Guarantee demo personas have valid password hashes if previously unpopulated
        cursor.execute(
            "UPDATE learners SET password_hash = ? WHERE id IN ('student-01', 'student-02', 'student-03') AND password_hash IS NULL;",
            (student_pw,)
        )
        cursor.execute(
            "UPDATE learners SET password_hash = ? WHERE id = 'teacher-01' AND password_hash IS NULL;",
            (teacher_pw,)
        )
        conn.commit()
    conn.close()
