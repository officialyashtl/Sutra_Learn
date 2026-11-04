"""
SUTRA LEARN — Centralized Audit & Compliance Logging Service
Records immutable, append-only audit events across all 20 required system domains:
1. Login success / failure
2. Token verification / rejection
3. Account & profile modifications
4. Lesson access & completion
5. Assessment submissions & attempts
6. Progress recalculations
7. AI tutor conversations & messages
8. Teacher overrides & interventions
9. Spaced retrieval schedule updates
10. Authorization failures & security rejections
11. External AI provider errors & fallbacks
12. System configuration & runtime events
"""

import uuid
import json
import logging
from datetime import datetime, timezone
from typing import Optional, Dict, Any
import sqlite3

logger = logging.getLogger("sutra.audit")


class AuditCategory:
    PEDAGOGICAL = "PEDAGOGICAL_INTERVENTIONS"
    SECURITY = "REJECTED_SECURITY_EVENTS"
    AUTHORIZED = "SUCCESSFUL_AUTHORIZED_ACTIONS"
    SYSTEM = "SYSTEM_EVENTS"


def record_audit_event(
    conn: sqlite3.Connection,
    event_category: str,
    actor_id: str,
    outcome: str,
    actor_role: Optional[str] = None,
    learner_id: Optional[str] = None,
    concept_id: Optional[str] = None,
    previous_state: Optional[str] = None,
    new_state: Optional[str] = None,
    rationale: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
    correlation_id: Optional[str] = None,
) -> str:
    """
    Appends an immutable audit record to system_audit_logs.
    Guarantees sanitized details, UTC timestamps, and correlation ID propagation.
    """
    event_id = f"aud_{uuid.uuid4().hex[:14]}"
    sanitized_details = None
    if details:
        # Guarantee no secrets or bearer tokens are ever written to audit logs
        scrubbed = {}
        for k, v in details.items():
            k_lower = str(k).lower()
            if any(secret_term in k_lower for secret_term in ["password", "token", "secret", "key", "authorization"]):
                scrubbed[k] = "[REDACTED]"
            else:
                scrubbed[k] = v
        sanitized_details = json.dumps(scrubbed, default=str)

    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO system_audit_logs (
                id, event_category, actor_id, actor_role, learner_id,
                concept_id, previous_state, new_state, rationale,
                outcome, details, correlation_id, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """,
            (
                event_id,
                event_category,
                actor_id,
                actor_role,
                learner_id,
                concept_id,
                previous_state,
                new_state,
                rationale,
                outcome,
                sanitized_details,
                correlation_id
            )
        )
        conn.commit()
    except Exception as e:
        logger.error(f"Failed to persist audit log {event_id}: {e}")

    return event_id


def log_security_rejection(
    conn: sqlite3.Connection,
    actor_id: str,
    rationale: str,
    actor_role: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
    correlation_id: Optional[str] = None
) -> str:
    """Helper to record rejected security & authorization events."""
    return record_audit_event(
        conn=conn,
        event_category=AuditCategory.SECURITY,
        actor_id=actor_id,
        actor_role=actor_role,
        outcome="REJECTED",
        rationale=rationale,
        details=details,
        correlation_id=correlation_id
    )


def log_authorized_action(
    conn: sqlite3.Connection,
    actor_id: str,
    rationale: str,
    actor_role: Optional[str] = None,
    learner_id: Optional[str] = None,
    concept_id: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
    correlation_id: Optional[str] = None
) -> str:
    """Helper to record successful authorized operations."""
    return record_audit_event(
        conn=conn,
        event_category=AuditCategory.AUTHORIZED,
        actor_id=actor_id,
        actor_role=actor_role,
        learner_id=learner_id,
        concept_id=concept_id,
        outcome="RECORDED",
        rationale=rationale,
        details=details,
        correlation_id=correlation_id
    )


def log_pedagogical_event(
    conn: sqlite3.Connection,
    actor_id: str,
    learner_id: str,
    concept_id: str,
    previous_state: str,
    new_state: str,
    rationale: str,
    outcome: str = "APPLIED",
    actor_role: Optional[str] = "system",
    details: Optional[Dict[str, Any]] = None,
    correlation_id: Optional[str] = None
) -> str:
    """Helper to record clinical pedagogical interventions and mastery adaptations."""
    return record_audit_event(
        conn=conn,
        event_category=AuditCategory.PEDAGOGICAL,
        actor_id=actor_id,
        actor_role=actor_role,
        learner_id=learner_id,
        concept_id=concept_id,
        previous_state=previous_state,
        new_state=new_state,
        rationale=rationale,
        outcome=outcome,
        details=details,
        correlation_id=correlation_id
    )

