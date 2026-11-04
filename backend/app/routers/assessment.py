"""
SUTRA LEARN - Assessment & Adaptive Recommendation API Router
Requires authenticated caller identity and enforces ownership of submissions.
"""

import uuid
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends, Request
from app.db.database import get_db_connection
from app.db import crud
from app.content.questions import QUESTIONS_REGISTRY
from app.content.concepts import CONCEPTS_REGISTRY
from app.engine.adaptive import AdaptiveEngine
from app.schemas import (
    AttemptCreate,
    AttemptResult,
    EvaluationRequest,
    RecommendationResponse
)
from app.auth import get_current_user
from app.services.audit import record_audit_event, AuditCategory

router = APIRouter(prefix="/api/v1", tags=["Assessment & Adaptation"])
engine = AdaptiveEngine()


@router.post("/sessions/start")
def start_assessment_session(
    data: Dict[str, str],
    current_user: Dict[str, Any] = Depends(get_current_user),
    conn=Depends(get_db_connection)
):
    learner_id = data.get("learner_id")
    concept_id = data.get("concept_id")
    if not learner_id or not concept_id:
        raise HTTPException(status_code=400, detail="learner_id and concept_id are required.")

    # Ownership check
    if current_user["id"] != learner_id and current_user["role"] != "teacher":
        raise HTTPException(status_code=403, detail="Cannot start assessment session for another learner.")

    if concept_id.upper() not in CONCEPTS_REGISTRY:
        raise HTTPException(status_code=404, detail=f"Concept '{concept_id}' not found.")

    session_id = str(uuid.uuid4())
    cursor = conn.cursor()
    crud.get_or_create_learner(conn, learner_id)
    cursor.execute(
        "INSERT INTO assessment_sessions (id, learner_id, concept_id) VALUES (?, ?, ?)",
        (session_id, learner_id, concept_id.upper())
    )
    conn.commit()
    return {"session_id": session_id, "learner_id": learner_id, "concept_id": concept_id.upper()}


@router.post("/attempts", response_model=AttemptResult)
def submit_attempt(
    attempt: AttemptCreate,
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user),
    conn=Depends(get_db_connection)
):
    """
    Submits a student's answer.
    Enforces that the authenticated user matches the attempt's learner_id.
    Enforces idempotency using attempt_id: duplicates return existing evaluation without re-inserting.
    """
    if current_user["id"] != attempt.learner_id and current_user["role"] != "teacher":
        raise HTTPException(status_code=403, detail="Cannot submit attempts on behalf of another learner.")

    q_id = attempt.question_id
    if q_id not in QUESTIONS_REGISTRY:
        raise HTTPException(status_code=404, detail=f"Question '{q_id}' not found.")

    q = QUESTIONS_REGISTRY[q_id]
    is_correct = (attempt.selected_option_id.upper() == q.correct_option_id.upper())

    misconception_tag = "none"
    misconception_explanation = None
    for opt in q.options:
        if opt.id.upper() == attempt.selected_option_id.upper():
            if not is_correct and opt.misconception_tag:
                misconception_tag = opt.misconception_tag.value
                misconception_explanation = opt.misconception_explanation
            break

    db_res = crud.record_attempt(
        conn=conn,
        attempt_id=attempt.attempt_id,
        learner_id=attempt.learner_id,
        question_id=q_id,
        concept_id=q.concept_id,
        selected_option_id=attempt.selected_option_id.upper(),
        is_correct=is_correct,
        hint_used=attempt.hint_used,
        misconception_tag=misconception_tag,
        cognitive_demand=q.cognitive_demand.value,
        session_id=attempt.session_id,
        client_timestamp=attempt.client_timestamp
    )

    final_is_correct = db_res["is_correct"] if db_res["is_duplicate"] else is_correct
    final_hint_used = db_res["hint_used"] if db_res["is_duplicate"] else attempt.hint_used
    final_selected = db_res["selected_option_id"] if db_res["is_duplicate"] else attempt.selected_option_id.upper()
    final_misconception = db_res["misconception_tag"] if db_res["is_duplicate"] else misconception_tag

    # Record attempt creation in audit trail
    corr_id = getattr(request.state, "correlation_id", None) if hasattr(request, "state") else None
    record_audit_event(
        conn=conn,
        event_category=AuditCategory.AUTHORIZED,
        actor_id=current_user["id"],
        actor_role=current_user.get("role"),
        learner_id=attempt.learner_id,
        concept_id=q.concept_id,
        outcome="RECORDED",
        rationale=f"Attempt submitted for {q_id} (correct={final_is_correct}, duplicate={db_res['is_duplicate']})",
        correlation_id=corr_id,
        details={
            "attempt_id": attempt.attempt_id,
            "question_id": q_id,
            "is_correct": final_is_correct,
            "hint_used": final_hint_used,
            "misconception_tag": final_misconception
        }
    )

    return AttemptResult(
        attempt_id=attempt.attempt_id,
        is_duplicate=db_res["is_duplicate"],
        is_correct=final_is_correct,
        hint_used=final_hint_used,
        selected_option_id=final_selected,
        correct_option_id=q.correct_option_id,
        explanation=q.explanation,
        misconception_tag=final_misconception,
        misconception_explanation=misconception_explanation,
        message=db_res["message"]
    )


@router.post("/recommendations/evaluate", response_model=RecommendationResponse)
def evaluate_concept_progress(
    req: EvaluationRequest,
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user),
    conn=Depends(get_db_connection)
):
    """
    Runs the deterministic adaptive engine over student attempt history.
    Enforces that caller can only evaluate their own progress (unless teacher).
    """
    if current_user["id"] != req.learner_id and current_user["role"] != "teacher":
        raise HTTPException(status_code=403, detail="Cannot evaluate adaptive progress for another learner.")

    concept_id = req.concept_id.upper()
    if concept_id not in CONCEPTS_REGISTRY:
        raise HTTPException(status_code=404, detail=f"Concept '{concept_id}' not found.")

    evidence = crud.get_attempts_for_learner_concept(conn, req.learner_id, concept_id)
    rec = engine.evaluate_learner_concept(concept_id, evidence)
    rec_id = crud.save_recommendation(conn, req.learner_id, concept_id, rec)

    # Record clinical adaptation outcome in audit trail
    corr_id = getattr(request.state, "correlation_id", None) if hasattr(request, "state") else None
    record_audit_event(
        conn=conn,
        event_category=AuditCategory.PEDAGOGICAL,
        actor_id=current_user["id"],
        actor_role=current_user.get("role"),
        learner_id=req.learner_id,
        concept_id=concept_id,
        outcome="APPLIED",
        rationale=f"Adaptive evaluation yielded {rec.outcome.value} (reason: {rec.reason_code})",
        correlation_id=corr_id,
        details={
            "recommendation_id": rec_id,
            "outcome": rec.outcome.value,
            "confidence": rec.confidence_score,
            "policy_version": rec.policy_version
        }
    )

    return RecommendationResponse(
        id=rec_id,
        learner_id=req.learner_id,
        concept_id=concept_id,
        outcome=rec.outcome.value,
        target_concept_id=rec.target_concept_id,
        target_concept_title=rec.target_concept_title,
        target_activity_type=rec.target_activity_type,
        target_activity_id=rec.target_activity_id,
        reason_code=rec.reason_code,
        explanation=rec.explanation,
        confidence_score=rec.confidence_score,
        evidence_summary=rec.evidence_summary,
        policy_version=rec.policy_version
    )
