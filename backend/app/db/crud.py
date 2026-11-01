"""
SUTRA LEARN - CRUD & Database Operations
Parameterized SQL queries ensuring safety, data integrity, and atomic transactions.
"""

import json
import sqlite3
import uuid
from typing import List, Optional, Dict, Any
from app.engine.adaptive import EvidenceRecord, Recommendation, LearningPathOutcome
from app.content.models import MisconceptionTag, CognitiveDemand


def get_or_create_learner(conn: sqlite3.Connection, learner_id: str, name: str = "Learner", role: str = "student") -> Dict[str, Any]:
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, grade, role, created_at FROM learners WHERE id = ?", (learner_id,))
    row = cursor.fetchone()
    if row:
        return dict(row)
    cursor.execute(
        "INSERT INTO learners (id, name, grade, role) VALUES (?, ?, 8, ?)",
        (learner_id, name, role)
    )
    conn.commit()
    return {"id": learner_id, "name": name, "grade": 8, "role": role}


def get_all_learners(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, grade, role, created_at FROM learners ORDER BY role DESC, name ASC")
    return [dict(row) for row in cursor.fetchall()]


def record_attempt(
    conn: sqlite3.Connection,
    attempt_id: str,
    learner_id: str,
    question_id: str,
    concept_id: str,
    selected_option_id: str,
    is_correct: bool,
    hint_used: bool = False,
    misconception_tag: str = "none",
    cognitive_demand: str = "procedural",
    session_id: Optional[str] = None,
    client_timestamp: Optional[str] = None
) -> Dict[str, Any]:
    """
    Idempotent attempt recording.
    If attempt_id already exists (e.g. from network retry or offline resend),
    returns the existing attempt without creating a duplicate.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT id, is_correct, hint_used, selected_option_id, misconception_tag, server_timestamp FROM attempts WHERE id = ?", (attempt_id,))
    existing = cursor.fetchone()
    if existing:
        return {
            "id": existing["id"],
            "is_duplicate": True,
            "is_correct": bool(existing["is_correct"]),
            "hint_used": bool(existing["hint_used"]),
            "selected_option_id": existing["selected_option_id"],
            "misconception_tag": existing["misconception_tag"],
            "message": "Attempt was already recorded (idempotent acknowledge)."
        }

    # Ensure learner exists
    get_or_create_learner(conn, learner_id)

    cursor.execute(
        """
        INSERT INTO attempts (
            id, session_id, learner_id, question_id, concept_id,
            selected_option_id, is_correct, hint_used, misconception_tag,
            cognitive_demand, client_timestamp, sync_status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'synced')
        """,
        (
            attempt_id,
            session_id,
            learner_id,
            question_id,
            concept_id,
            selected_option_id,
            1 if is_correct else 0,
            1 if hint_used else 0,
            misconception_tag,
            cognitive_demand,
            client_timestamp
        )
    )
    conn.commit()
    return {
        "id": attempt_id,
        "is_duplicate": False,
        "is_correct": is_correct,
        "hint_used": hint_used,
        "selected_option_id": selected_option_id,
        "misconception_tag": misconception_tag,
        "message": "Attempt successfully recorded."
    }


def get_attempts_for_learner_concept(
    conn: sqlite3.Connection,
    learner_id: str,
    concept_id: str
) -> List[EvidenceRecord]:
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, question_id, concept_id, is_correct, hint_used,
               selected_option_id, misconception_tag, cognitive_demand, server_timestamp
        FROM attempts
        WHERE learner_id = ? AND concept_id = ?
        ORDER BY server_timestamp ASC
        """,
        (learner_id, concept_id)
    )
    records = []
    for row in cursor.fetchall():
        records.append(EvidenceRecord(
            attempt_id=row["id"],
            question_id=row["question_id"],
            concept_id=row["concept_id"],
            is_correct=bool(row["is_correct"]),
            hint_used=bool(row["hint_used"]),
            selected_option_id=row["selected_option_id"],
            misconception_tag=MisconceptionTag(row["misconception_tag"]) if row["misconception_tag"] in [m.value for m in MisconceptionTag] else MisconceptionTag.NONE,
            cognitive_demand=CognitiveDemand(row["cognitive_demand"]) if row["cognitive_demand"] in [c.value for c in CognitiveDemand] else CognitiveDemand.PROCEDURAL,
            timestamp=row["server_timestamp"]
        ))
    return records


def save_recommendation(
    conn: sqlite3.Connection,
    learner_id: str,
    concept_id: str,
    rec: Recommendation
) -> str:
    rec_id = str(uuid.uuid4())
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO recommendations (
            id, learner_id, concept_id, outcome, target_concept_id,
            target_concept_title, target_activity_type, target_activity_id,
            reason_code, explanation, confidence_score, evidence_summary_json,
            policy_version
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            rec_id,
            learner_id,
            concept_id,
            rec.outcome.value,
            rec.target_concept_id,
            rec.target_concept_title,
            rec.target_activity_type,
            rec.target_activity_id,
            rec.reason_code,
            rec.explanation,
            rec.confidence_score,
            json.dumps(rec.evidence_summary),
            rec.policy_version
        )
    )

    # Update concept_progress
    summary = rec.evidence_summary
    total_distinct = summary.get("total_distinct", 0) if isinstance(summary, dict) else 0
    unassisted = summary.get("unassisted_correct", 0) if isinstance(summary, dict) else 0
    assisted = summary.get("assisted_correct", 0) if isinstance(summary, dict) else 0
    accuracy = summary.get("unassisted_accuracy", 0.0) if isinstance(summary, dict) else 0.0

    status = "in_progress"
    if rec.outcome == LearningPathOutcome.STRETCH:
        status = "mastered"
    elif rec.outcome == LearningPathOutcome.BRIDGE_BACK or rec.outcome == LearningPathOutcome.TEACHER_REVIEW:
        status = "needs_reinforcement"

    cursor.execute(
        """
        INSERT INTO concept_progress (
            learner_id, concept_id, status, unassisted_correct,
            assisted_correct, total_attempts, mastery_percentage,
            last_recommended_outcome, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(learner_id, concept_id) DO UPDATE SET
            status = excluded.status,
            unassisted_correct = excluded.unassisted_correct,
            assisted_correct = excluded.assisted_correct,
            total_attempts = excluded.total_attempts,
            mastery_percentage = excluded.mastery_percentage,
            last_recommended_outcome = excluded.last_recommended_outcome,
            updated_at = CURRENT_TIMESTAMP
        """,
        (
            learner_id,
            concept_id,
            status,
            unassisted,
            assisted,
            total_distinct,
            float(accuracy) * 100.0,
            rec.outcome.value
        )
    )
    conn.commit()
    return rec_id


def get_learner_progress(conn: sqlite3.Connection, learner_id: str) -> List[Dict[str, Any]]:
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT concept_id, status, unassisted_correct, assisted_correct,
               total_attempts, mastery_percentage, last_recommended_outcome, updated_at
        FROM concept_progress
        WHERE learner_id = ?
        ORDER BY concept_id ASC
        """,
        (learner_id,)
    )
    return [dict(row) for row in cursor.fetchall()]


def record_teacher_override(
    conn: sqlite3.Connection,
    learner_id: str,
    concept_id: str,
    previous_outcome: str,
    overridden_outcome: str,
    reason: str,
    teacher_id: str
) -> Dict[str, Any]:
    if not reason or len(reason.strip()) < 5:
        raise ValueError("A clear, substantive reason (at least 5 characters) is required for any pedagogical override.")

    override_id = str(uuid.uuid4())
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO teacher_overrides (
            id, learner_id, concept_id, previous_outcome,
            overridden_outcome, reason, teacher_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (override_id, learner_id, concept_id, previous_outcome, overridden_outcome, reason, teacher_id)
    )

    # Log to unified system audit table
    cursor.execute(
        """
        INSERT INTO system_audit_logs (
            id, event_category, actor_id, actor_role, learner_id, concept_id,
            previous_state, new_state, rationale, outcome, details
        ) VALUES (?, 'PEDAGOGICAL_INTERVENTIONS', ?, 'teacher', ?, ?, ?, ?, ?, 'APPLIED', 'Clinical educator override verified and applied.')
        """,
        (override_id, teacher_id, learner_id, concept_id, previous_outcome, overridden_outcome, reason.strip())
    )

    # Update concept progress
    new_status = "in_progress"
    if overridden_outcome == "STRETCH":
        new_status = "mastered"
    elif overridden_outcome == "BRIDGE_BACK":
        new_status = "needs_reinforcement"

    cursor.execute(
        """
        UPDATE concept_progress
        SET status = ?, last_recommended_outcome = ?, updated_at = CURRENT_TIMESTAMP
        WHERE learner_id = ? AND concept_id = ?
        """,
        (new_status, overridden_outcome, learner_id, concept_id)
    )
    conn.commit()
    return {
        "override_id": override_id,
        "learner_id": learner_id,
        "concept_id": concept_id,
        "overridden_outcome": overridden_outcome,
        "reason": reason,
        "teacher_id": teacher_id
    }


def get_intervention_effectiveness(conn: sqlite3.Connection, override_id: str) -> Dict[str, Any]:
    """
    Measures quantitative learning improvement following a clinical educator intervention.
    Calculates before vs after accuracy, misconception resolution, and retention status.
    """
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, learner_id, concept_id, previous_outcome, overridden_outcome, reason, created_at FROM teacher_overrides WHERE id = ?",
        (override_id,)
    )
    override = cursor.fetchone()
    if not override:
        raise ValueError(f"Intervention override '{override_id}' not found.")

    learner_id = override["learner_id"]
    concept_id = override["concept_id"]
    ts = override["created_at"]

    # Before attempts
    cursor.execute(
        "SELECT is_correct, hint_used, misconception_tag FROM attempts WHERE learner_id = ? AND concept_id = ? AND server_timestamp < ?",
        (learner_id, concept_id, ts)
    )
    before_attempts = cursor.fetchall()

    # After attempts
    cursor.execute(
        "SELECT is_correct, hint_used, misconception_tag FROM attempts WHERE learner_id = ? AND concept_id = ? AND server_timestamp >= ?",
        (learner_id, concept_id, ts)
    )
    after_attempts = cursor.fetchall()

    before_tot = len(before_attempts)
    before_corr = sum(1 for a in before_attempts if a["is_correct"] == 1)
    before_acc = round((before_corr / before_tot) * 100, 1) if before_tot > 0 else None

    after_tot = len(after_attempts)
    after_corr = sum(1 for a in after_attempts if a["is_correct"] == 1)
    after_acc = round((after_corr / after_tot) * 100, 1) if after_tot > 0 else None

    acc_delta = round(after_acc - before_acc, 1) if (after_acc is not None and before_acc is not None) else None

    before_misc = sum(1 for a in before_attempts if a["misconception_tag"] and a["misconception_tag"] != "none")
    after_misc = sum(1 for a in after_attempts if a["misconception_tag"] and a["misconception_tag"] != "none")

    retention_status = "PENDING"
    if after_acc is not None:
        if after_acc >= 85.0 and after_tot >= 2:
            retention_status = "RETAINED"
        elif after_acc < 60.0:
            retention_status = "NEEDS REINFORCEMENT"
        else:
            retention_status = "REASSESSED"

    return {
        "intervention_id": override_id,
        "learner_id": learner_id,
        "concept_id": concept_id,
        "overridden_outcome": override["overridden_outcome"],
        "reason": override["reason"],
        "intervention_timestamp": ts,
        "before": {
            "attempts_count": before_tot,
            "accuracy_pct": before_acc,
            "misconceptions_count": before_misc
        },
        "after": {
            "attempts_count": after_tot,
            "accuracy_pct": after_acc,
            "misconceptions_count": after_misc
        },
        "accuracy_delta_pct": acc_delta,
        "misconceptions_resolved": max(0, before_misc - after_misc),
        "retention_status": retention_status
    }


def get_teacher_cohort_summary(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT l.id AS learner_id, l.name, l.grade,
               COALESCE(att.total_attempts, 0) as total_attempts,
               COALESCE(att.total_correct, 0) as total_correct,
               rec.latest_outcome,
               rec.last_evaluated_at,
               EXISTS(
                   SELECT 1 FROM recommendations r2
                   WHERE r2.learner_id = l.id AND r2.outcome = 'TEACHER_REVIEW'
               ) as needs_review
        FROM learners l
        LEFT JOIN (
            SELECT learner_id,
                   COUNT(DISTINCT id) as total_attempts,
                   COUNT(DISTINCT CASE WHEN is_correct = 1 THEN id ELSE NULL END) as total_correct
            FROM attempts
            GROUP BY learner_id
        ) att ON l.id = att.learner_id
        LEFT JOIN (
            SELECT r1.learner_id,
                   r1.outcome as latest_outcome,
                   r1.created_at as last_evaluated_at
            FROM recommendations r1
            INNER JOIN (
                SELECT learner_id, MAX(created_at) as max_created
                FROM recommendations
                GROUP BY learner_id
            ) r_max ON r1.learner_id = r_max.learner_id AND r1.created_at = r_max.max_created
        ) rec ON l.id = rec.learner_id
        WHERE l.role = 'student'
        ORDER BY needs_review DESC, l.name ASC
        """
    )
    rows = []
    for r in cursor.fetchall():
        d = dict(r)
        tot = max(0, d.get("total_attempts") or 0)
        corr = max(0, d.get("total_correct") or 0)
        if corr > tot:
            corr = tot
        d["total_attempts"] = tot
        d["total_correct"] = corr
        d["accuracy_percentage"] = round((corr / tot) * 100, 1) if tot > 0 else None
        rows.append(d)
    return rows


def get_teacher_overrides_audit(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT t.id, t.learner_id, l.name as learner_name, t.concept_id,
               t.previous_outcome, t.overridden_outcome, t.reason,
               t.teacher_id, t.created_at
        FROM teacher_overrides t
        JOIN learners l ON t.learner_id = l.id
        ORDER BY t.created_at DESC
        """
    )
    return [dict(row) for row in cursor.fetchall()]


def get_categorized_audit_events(conn: sqlite3.Connection, category: str = None) -> List[Dict[str, Any]]:
    cursor = conn.cursor()
    query = """
    SELECT * FROM (
        SELECT
            t.id,
            'PEDAGOGICAL_INTERVENTIONS' as event_category,
            t.teacher_id as actor_id,
            'teacher' as actor_role,
            t.learner_id,
            l.name as learner_name,
            t.concept_id,
            t.previous_outcome as previous_state,
            t.overridden_outcome as new_state,
            t.reason as rationale,
            'APPLIED' as outcome,
            'Clinical educator override verified and applied.' as details,
            t.created_at
        FROM teacher_overrides t
        JOIN learners l ON t.learner_id = l.id
        UNION ALL
        SELECT
            s.id,
            s.event_category,
            s.actor_id,
            s.actor_role,
            s.learner_id,
            COALESCE(l2.name, s.learner_id) as learner_name,
            s.concept_id,
            s.previous_state,
            s.new_state,
            s.rationale,
            s.outcome,
            s.details,
            s.created_at
        FROM system_audit_logs s
        LEFT JOIN learners l2 ON s.learner_id = l2.id
        WHERE s.id NOT IN (SELECT id FROM teacher_overrides)
    )
    ORDER BY created_at DESC
    """
    cursor.execute(query)
    all_events = [dict(row) for row in cursor.fetchall()]
    if category and category != "ALL":
        all_events = [e for e in all_events if e["event_category"] == category]
    return all_events



def get_teacher_concept_analytics(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT concept_id,
               COUNT(*) as total_attempts,
               SUM(CASE WHEN is_correct = 1 THEN 1 ELSE 0 END) as total_correct,
               SUM(CASE WHEN hint_used = 1 THEN 1 ELSE 0 END) as total_assisted,
               SUM(CASE WHEN is_correct = 1 AND hint_used = 0 THEN 1 ELSE 0 END) as unassisted_correct
        FROM attempts
        GROUP BY concept_id
        """
    )
    data = []
    for row in cursor.fetchall():
        total = row["total_attempts"] or 0
        correct = row["total_correct"] or 0
        accuracy = round((correct / total) * 100, 1) if total > 0 else 0.0

        # Fetch top misconceptions for this concept
        cur_m = conn.cursor()
        cur_m.execute(
            """
            SELECT misconception_tag, COUNT(*) as cnt
            FROM attempts
            WHERE concept_id = ? AND misconception_tag != 'none'
            GROUP BY misconception_tag
            ORDER BY cnt DESC
            LIMIT 3
            """,
            (row["concept_id"],)
        )
        misconceptions = [f"{m['misconception_tag']} ({m['cnt']})" for m in cur_m.fetchall()]

        data.append({
            "concept_id": row["concept_id"],
            "total_attempts": total,
            "total_correct": correct,
            "total_assisted": row["total_assisted"] or 0,
            "unassisted_correct": row["unassisted_correct"] or 0,
            "accuracy_percentage": accuracy,
            "top_misconceptions": misconceptions,
        })
    return data


# ===========================================================================
# SUTRA AI — Conversation & Message Storage CRUD
# ===========================================================================

def create_ai_conversation(
    conn: sqlite3.Connection,
    conversation_id: str,
    owner_id: str,
    owner_role: str,
    title: str,
    conversation_type: str = "tutor",
    concept_id: Optional[str] = None
) -> Dict[str, Any]:
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO ai_conversations (id, owner_id, owner_role, conversation_type, title, concept_id)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (conversation_id, owner_id, owner_role, conversation_type, title, concept_id)
    )
    conn.commit()
    return {
        "id": conversation_id,
        "owner_id": owner_id,
        "owner_role": owner_role,
        "conversation_type": conversation_type,
        "title": title,
        "concept_id": concept_id,
    }


def get_user_ai_conversations(
    conn: sqlite3.Connection,
    owner_id: str,
    conversation_type: str = "tutor"
) -> List[Dict[str, Any]]:
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, owner_id, owner_role, conversation_type, title, concept_id, created_at, updated_at
        FROM ai_conversations
        WHERE owner_id = ? AND conversation_type = ?
        ORDER BY updated_at DESC
        """,
        (owner_id, conversation_type)
    )
    return [dict(row) for row in cursor.fetchall()]


def get_ai_conversation(
    conn: sqlite3.Connection,
    conversation_id: str
) -> Optional[Dict[str, Any]]:
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, owner_id, owner_role, conversation_type, title, concept_id, created_at, updated_at
        FROM ai_conversations
        WHERE id = ?
        """,
        (conversation_id,)
    )
    row = cursor.fetchone()
    return dict(row) if row else None


def get_ai_messages(
    conn: sqlite3.Connection,
    conversation_id: str
) -> List[Dict[str, Any]]:
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, conversation_id, sender_role, content, response_type, hints_json, concept_id,
               requires_follow_up, provider_metadata, created_at
        FROM ai_messages
        WHERE conversation_id = ?
        ORDER BY created_at ASC
        """,
        (conversation_id,)
    )
    results = []
    for r in cursor.fetchall():
        d = dict(r)
        if d.get("hints_json"):
            try:
                d["hints"] = json.loads(d["hints_json"])
            except Exception:
                d["hints"] = []
        else:
            d["hints"] = []
        if d.get("provider_metadata"):
            try:
                d["provider_metadata"] = json.loads(d["provider_metadata"])
            except Exception:
                pass
        results.append(d)
    return results


def add_ai_message(
    conn: sqlite3.Connection,
    message_id: str,
    conversation_id: str,
    sender_role: str,
    content: str,
    response_type: str = "standard",
    hints: Optional[List[str]] = None,
    concept_id: Optional[str] = None,
    requires_follow_up: bool = False,
    provider_metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    hints_json = json.dumps(hints) if hints else None
    metadata_json = json.dumps(provider_metadata) if provider_metadata else None
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO ai_messages (
            id, conversation_id, sender_role, content, response_type,
            hints_json, concept_id, requires_follow_up, provider_metadata
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            message_id,
            conversation_id,
            sender_role,
            content,
            response_type,
            hints_json,
            concept_id,
            1 if requires_follow_up else 0,
            metadata_json
        )
    )
    cursor.execute(
        "UPDATE ai_conversations SET updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (conversation_id,)
    )
    conn.commit()
    return {
        "id": message_id,
        "conversation_id": conversation_id,
        "sender_role": sender_role,
        "content": content,
        "response_type": response_type,
        "hints": hints or [],
        "concept_id": concept_id,
        "requires_follow_up": requires_follow_up,
        "provider_metadata": provider_metadata or {}
    }


def delete_ai_conversation(
    conn: sqlite3.Connection,
    conversation_id: str,
    owner_id: str
) -> bool:
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM ai_conversations WHERE id = ? AND owner_id = ?",
        (conversation_id, owner_id)
    )
    conn.commit()
    return cursor.rowcount > 0


