"""
SUTRA LEARN - Learners & Progress API Router
Enforces resource ownership authorization using cryptographic Bearer tokens.
Cross-student snooping is blocked with 403 Forbidden.
"""

from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException, Depends
from app.db.database import get_db_connection
from app.db import crud
from app.auth import get_current_user
from app.services.metrics import calculate_learner_metrics

router = APIRouter(prefix="/api/v1/learners", tags=["Learners"])


def verify_learner_ownership(target_learner_id: str, current_user: Dict[str, Any]):
    # Allow if caller is the learner themselves or holds a verified teacher role
    if current_user["id"] == target_learner_id:
        return
    if current_user["role"] == "teacher":
        return

    raise HTTPException(
        status_code=403,
        detail=f"Forbidden: Authenticated user '{current_user['id']}' is not authorized to access records of '{target_learner_id}'."
    )


@router.get("", response_model=List[Dict[str, Any]])
def list_learners(conn=Depends(get_db_connection)):
    """List available learner and teacher profiles (public directory for persona selection)."""
    return crud.get_all_learners(conn)


@router.get("/{learner_id}/progress")
def get_progress(
    learner_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
    conn=Depends(get_db_connection)
):
    verify_learner_ownership(learner_id, current_user)
    crud.get_or_create_learner(conn, learner_id)
    progress_rows = crud.get_learner_progress(conn, learner_id)
    return {
        "learner_id": learner_id,
        "progress": progress_rows
    }


@router.get("/{learner_id}/attempts")
def get_learner_attempts(
    learner_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
    conn=Depends(get_db_connection)
):
    verify_learner_ownership(learner_id, current_user)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT a.id, a.question_id, a.concept_id, a.selected_option_id,
               a.is_correct, a.hint_used, a.misconception_tag, a.server_timestamp
        FROM attempts a
        WHERE a.learner_id = ?
        ORDER BY a.server_timestamp DESC
        """,
        (learner_id,)
    )
    rows = [dict(r) for r in cursor.fetchall()]
    return {
        "learner_id": learner_id,
        "total_attempts": len(rows),
        "attempts": rows
    }


@router.get("/{learner_id}/metrics")
def get_learner_metrics_endpoint(
    learner_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
    conn=Depends(get_db_connection)
):
    """
    Canonical metric engine endpoint for student analytics.
    Serves identical 56 metrics to Student Home, Progress, Insights, and Teacher Dossier.
    """
    verify_learner_ownership(learner_id, current_user)
    return calculate_learner_metrics(conn, learner_id)
