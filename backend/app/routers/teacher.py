"""
SUTRA LEARN - Teacher Workspace & Oversight API Router
Server-enforced role authorization using cryptographically validated Bearer tokens.
Direct caller-supplied identity headers (e.g. x-teacher-id) are rejected.
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from app.db.database import get_db_connection
from app.db import crud
from app.schemas import TeacherOverrideRequest
from app.auth import require_teacher
from app.services.metrics import calculate_cohort_metrics

router = APIRouter(prefix="/api/v1/teacher", tags=["Teacher Oversight"])


@router.get("/cohort", response_model=List[Dict[str, Any]])
def get_cohort(
    current_teacher: Dict[str, Any] = Depends(require_teacher),
    conn=Depends(get_db_connection)
):
    """
    Cohort summary for verified teachers only.
    Protected by cryptographic token; caller header spoofing is rejected.
    """
    return crud.get_teacher_cohort_summary(conn)


@router.get("/analytics/concepts", response_model=List[Dict[str, Any]])
def get_concept_analytics(
    current_teacher: Dict[str, Any] = Depends(require_teacher),
    conn=Depends(get_db_connection)
):
    """
    Concept difficulty & misconception analytics across all attempts.
    Protected by teacher role authorization.
    """
    return crud.get_teacher_concept_analytics(conn)


@router.get("/overrides", response_model=List[Dict[str, Any]])
def list_overrides(
    current_teacher: Dict[str, Any] = Depends(require_teacher),
    conn=Depends(get_db_connection)
):
    """Full audit log of clinical pedagogical overrides."""
    return crud.get_teacher_overrides_audit(conn)


@router.get("/interventions/{override_id}/effectiveness")
def get_intervention_outcome(
    override_id: str,
    current_teacher: Dict[str, Any] = Depends(require_teacher),
    conn=Depends(get_db_connection)
):
    """
    Measures quantitative learning improvement and retention following a teacher intervention.
    """
    try:
        return crud.get_intervention_effectiveness(conn, override_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/audit", response_model=List[Dict[str, Any]])
def list_categorized_audit(
    category: Optional[str] = Query(None, description="Event category filter"),
    current_teacher: Dict[str, Any] = Depends(require_teacher),
    conn=Depends(get_db_connection)
):
    """
    Categorized audit trail separating:
    - PEDAGOGICAL_INTERVENTIONS
    - REJECTED_SECURITY_EVENTS
    - SUCCESSFUL_AUTHORIZED_ACTIONS
    - SYSTEM_EVENTS
    """
    return crud.get_categorized_audit_events(conn, category=category)



@router.post("/override")
def apply_override(
    req: TeacherOverrideRequest,
    current_teacher: Dict[str, Any] = Depends(require_teacher),
    conn=Depends(get_db_connection)
):
    """
    Applies an authorized manual override to a student's learning path.
    Requires verified teacher token and substantive clinical rationale (>= 5 chars).
    """
    try:
        result = crud.record_teacher_override(
            conn=conn,
            learner_id=req.learner_id,
            concept_id=req.concept_id.upper(),
            previous_outcome=req.previous_outcome,
            overridden_outcome=req.overridden_outcome,
            reason=req.reason,
            teacher_id=current_teacher["id"]
        )
        return {
            "status": "success",
            "message": "Pedagogical override applied and recorded in compliance audit log.",
            "data": result
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/metrics")
def get_teacher_cohort_metrics(
    current_teacher: Dict[str, Any] = Depends(require_teacher),
    conn=Depends(get_db_connection)
):
    """
    Canonical cohort metrics endpoint for educator intelligence.
    Serves aggregated analytics across the entire student roster.
    """
    return calculate_cohort_metrics(conn)
