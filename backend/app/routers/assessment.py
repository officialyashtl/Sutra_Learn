"""
SUTRA LEARN - Assessment & Adaptive Recommendation API Router
Requires authenticated caller identity and enforces ownership of submissions.
"""

import uuid
import logging
import asyncio
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
from fastapi import APIRouter, HTTPException, Depends, Request
from app.db.database import get_db_connection
from app.db import crud
from app.content.questions import QUESTIONS_REGISTRY, get_questions_by_concept
from app.content.concepts import CONCEPTS_REGISTRY, get_concept, get_all_concepts
from app.content.models import MisconceptionTag
from app.engine.adaptive import AdaptiveEngine, EvidenceRecord, LearningPathOutcome
from app.schemas import (
    AttemptCreate,
    AttemptResult,
    EvaluationRequest,
    RecommendationResponse,
    AssessmentCompleteRequest,
    QuestionResultDetail,
    AssessmentResultResponse
)
from app.auth import get_current_user
from app.services.audit import record_audit_event, AuditCategory
from app.ai.assessment_guidance import generate_assessment_guidance

logger = logging.getLogger("sutra.assessment")
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


@router.post("/assessments/complete", response_model=AssessmentResultResponse)
async def complete_assessment(
    req: AssessmentCompleteRequest,
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user),
    conn=Depends(get_db_connection)
):
    """
    Evaluates, scores, persists, and provides personalized Gemini learning guidance
    for an entire assessment.
    Enforces that the caller can only submit on their own behalf.
    Updates concept progress, checks prerequisites, and unlocks next lesson progression.
    """
    learner_id = current_user["id"]
    concept_id = req.concept_id.upper()

    if concept_id not in CONCEPTS_REGISTRY:
        raise HTTPException(status_code=404, detail=f"Concept '{concept_id}' not found.")

    concept = get_concept(concept_id)
    questions = get_questions_by_concept(concept_id)
    if not questions:
        raise HTTPException(status_code=404, detail=f"No questions found for concept '{concept_id}'.")

    # Idempotency: If this session was already completed, return existing result
    if req.session_id:
        existing = crud.get_latest_assessment_result(conn, learner_id, concept_id)
        if existing and existing.get("session_id") == req.session_id:
            existing["concept_title"] = concept.title if concept else concept_id
            return AssessmentResultResponse(**existing)

    # 1. Process and record submissions if provided
    submissions_map = {}
    if req.submissions:
        for sub in req.submissions:
            q_id = sub.question_id
            if q_id not in QUESTIONS_REGISTRY:
                continue
            q = QUESTIONS_REGISTRY[q_id]
            is_correct = (sub.selected_option_id.upper() == q.correct_option_id.upper())

            misc_tag = "none"
            misc_explanation = None
            for opt in q.options:
                if opt.id.upper() == sub.selected_option_id.upper():
                    if not is_correct and opt.misconception_tag:
                        misc_tag = opt.misconception_tag.value
                        misc_explanation = opt.misconception_explanation
                    break

            att_id = f"att-{uuid.uuid4()}"
            crud.record_attempt(
                conn=conn,
                attempt_id=att_id,
                learner_id=learner_id,
                question_id=q_id,
                concept_id=concept_id,
                selected_option_id=sub.selected_option_id.upper(),
                is_correct=is_correct,
                hint_used=sub.hint_used,
                misconception_tag=misc_tag,
                cognitive_demand=q.cognitive_demand.value,
                session_id=req.session_id,
                client_timestamp=sub.client_timestamp
            )
            submissions_map[q_id] = {
                "selected_option_id": sub.selected_option_id.upper(),
                "is_correct": is_correct,
                "hint_used": sub.hint_used,
                "misconception_tag": misc_tag,
                "misconception_explanation": misc_explanation
            }

    # 2. Retrieve all latest attempts for this learner and concept
    attempts = crud.get_attempts_for_learner_concept(conn, learner_id, concept_id)
    attempts_by_qid = {}
    for att in attempts:
        att_dict = att.model_dump() if hasattr(att, "model_dump") else (dict(att) if not isinstance(att, dict) else att)
        qid = att_dict.get("question_id")
        if qid and qid not in attempts_by_qid:
            attempts_by_qid[qid] = att_dict

    # 3. Grade each question
    questions_detail: List[QuestionResultDetail] = []
    correct_count = 0
    misconceptions_detected = []
    missed_questions = []

    for q in questions:
        att = submissions_map.get(q.id) or attempts_by_qid.get(q.id)
        if att:
            sel_opt_id = att.get("selected_option_id", "").upper()
            is_corr = bool(att.get("is_correct"))
            hint_used = bool(att.get("hint_used"))
            misc_tag = att.get("misconception_tag", "none")
            misc_exp = att.get("misconception_explanation")
        else:
            sel_opt_id = ""
            is_corr = False
            hint_used = False
            misc_tag = "none"
            misc_exp = None

        if is_corr:
            correct_count += 1
        else:
            if misc_tag and misc_tag != "none":
                misconceptions_detected.append(misc_tag)
            missed_questions.append({
                "question_id": q.id,
                "prompt": q.prompt,
                "selected_option_id": sel_opt_id,
                "selected_option_text": next((o.text for o in q.options if o.id.upper() == sel_opt_id), ""),
                "correct_option_id": q.correct_option_id,
                "correct_option_text": next((o.text for o in q.options if o.id.upper() == q.correct_option_id.upper()), ""),
                "misconception_tag": misc_tag
            })

        sel_text = next((o.text for o in q.options if o.id.upper() == sel_opt_id), "No answer selected")
        corr_text = next((o.text for o in q.options if o.id.upper() == q.correct_option_id.upper()), "")

        options_list = [{"id": o.id, "text": o.text} for o in q.options]

        questions_detail.append(QuestionResultDetail(
            question_id=q.id,
            prompt=q.prompt,
            equation_display=q.equation_display,
            difficulty=q.difficulty,
            cognitive_demand=q.cognitive_demand.value,
            selected_option_id=sel_opt_id,
            selected_option_text=sel_text,
            correct_option_id=q.correct_option_id,
            correct_option_text=corr_text,
            is_correct=is_corr,
            hint_used=hint_used,
            misconception_tag=misc_tag,
            misconception_explanation=misc_exp,
            explanation=q.explanation,
            options=options_list
        ))

    total_questions = len(questions)
    percentage = round((correct_count / total_questions) * 100.0, 1) if total_questions > 0 else 0.0
    passed = percentage >= 66.0

    # 4. Deterministic Adaptive Engine Evaluation
    evidence_records = []
    for q in questions:
        att = submissions_map.get(q.id) or attempts_by_qid.get(q.id)
        if att:
            misc_enum = MisconceptionTag.NONE
            try:
                misc_enum = MisconceptionTag(att.get("misconception_tag", "none"))
            except Exception:
                pass
            evidence_records.append(EvidenceRecord(
                attempt_id=att.get("attempt_id", f"att-{q.id}"),
                question_id=q.id,
                concept_id=concept_id,
                is_correct=bool(att.get("is_correct")),
                hint_used=bool(att.get("hint_used")),
                selected_option_id=att.get("selected_option_id", "A"),
                misconception_tag=misc_enum,
                cognitive_demand=q.cognitive_demand
            ))

    rec = engine.evaluate_learner_concept(concept_id, evidence_records)
    crud.save_recommendation(conn, learner_id, concept_id, rec)

    # 5. Determine Next Lesson Progression
    all_concepts = get_all_concepts()
    all_progress = crud.get_learner_progress(conn, learner_id)
    progress_status_map = {p["concept_id"]: p["status"] for p in all_progress}
    # Update current concept status in map
    current_status = "mastered" if passed else "needs_reinforcement"
    progress_status_map[concept_id] = current_status

    next_concept_id = None
    next_concept_title = None
    can_advance = False

    if passed or rec.outcome == LearningPathOutcome.STRETCH:
        # Check downstream concepts in curriculum order where concept_id is a prerequisite
        for c in all_concepts:
            if c.id == concept_id:
                continue
            if c.prerequisites and concept_id in c.prerequisites:
                prereqs_ok = all(
                    progress_status_map.get(pid) in ("in_progress", "mastered")
                    for pid in c.prerequisites
                )
                if prereqs_ok:
                    next_concept_id = c.id
                    next_concept_title = c.title
                    can_advance = True
                    break

        if not next_concept_id:
            for c in all_concepts:
                if c.id != concept_id and progress_status_map.get(c.id) != "mastered":
                    prereqs_ok = all(
                        progress_status_map.get(pid) in ("in_progress", "mastered")
                        for pid in c.prerequisites
                    ) if c.prerequisites else True
                    if prereqs_ok:
                        next_concept_id = c.id
                        next_concept_title = c.title
                        can_advance = True
                        break
    else:
        if rec.outcome == LearningPathOutcome.BRIDGE_BACK:
            next_concept_id = rec.target_concept_id
            next_concept_title = rec.target_concept_title
            can_advance = False
        else:
            next_concept_id = concept_id
            next_concept_title = concept.title
            can_advance = False

    # 6. Build Initial Authoritative Pedagogical Guidance (Instant, 0ms, Zero Cloud Dependency)
    initial_guidance = {
        "summary": f"Assessment completed for {concept.title}. You scored {correct_count} of {total_questions} ({percentage}%).",
        "strengths": [f"Demonstrated competency in {concept.title}"] if passed else [],
        "focus_area": f"Reinforce {concept.title} foundational steps." if not passed else "Ready to progress to next concept.",
        "action_step": f"Continue to {next_concept_title}." if can_advance else f"Review {concept.title} lesson materials and worked examples.",
        "provider": "sutra_deterministic",
        "is_fallback": True,
        "is_generating": False
    }

    # 7. Persist Assessment Result Immediately (Atomic DB Commit BEFORE Gemini)
    result_id = f"res-{uuid.uuid4()}"
    crud.save_assessment_result(
        conn=conn,
        result_id=result_id,
        learner_id=learner_id,
        concept_id=concept_id,
        score=correct_count,
        total_questions=total_questions,
        percentage=percentage,
        passed=passed,
        outcome=rec.outcome.value,
        questions_detail=[qd.model_dump() for qd in questions_detail],
        misconceptions=list(set(misconceptions_detected)),
        ai_guidance=initial_guidance,
        session_id=req.session_id,
        next_concept_id=next_concept_id,
        next_concept_title=next_concept_title,
        can_advance=can_advance
    )

    # 8. Record audit log
    corr_id = getattr(request.state, "correlation_id", None) if hasattr(request, "state") else None
    record_audit_event(
        conn=conn,
        event_category=AuditCategory.PEDAGOGICAL,
        actor_id=learner_id,
        actor_role=current_user.get("role"),
        learner_id=learner_id,
        concept_id=concept_id,
        outcome="COMPLETED",
        rationale=f"Assessment completed for {concept_id}: score {correct_count}/{total_questions} ({percentage}%), outcome {rec.outcome.value}",
        correlation_id=corr_id,
        details={
            "result_id": result_id,
            "score": correct_count,
            "total": total_questions,
            "passed": passed,
            "outcome": rec.outcome.value,
            "can_advance": can_advance,
            "ai_provider": "sutra_deterministic"
        }
    )

    # 9. Asynchronous Gemini Guidance Attempt (Bounded 2.5s Timeout - Never Blocks Saved Result)
    ai_guidance = initial_guidance
    try:
        gemini_task = generate_assessment_guidance(
            concept_id=concept_id,
            score=correct_count,
            total_questions=total_questions,
            percentage=percentage,
            passed=passed,
            outcome=rec.outcome.value,
            missed_questions=missed_questions,
            misconceptions=list(set(misconceptions_detected))
        )
        gemini_res = await asyncio.wait_for(gemini_task, timeout=2.5)
        if gemini_res and isinstance(gemini_res, dict):
            ai_guidance = gemini_res
            crud.update_assessment_result_guidance(conn, result_id, ai_guidance)
    except Exception as exc:
        logger.info(f"Gemini guidance deferred or timed out ({exc}); initial deterministic guidance safely preserved.")

    return AssessmentResultResponse(
        id=result_id,
        session_id=req.session_id,
        learner_id=learner_id,
        concept_id=concept_id,
        concept_title=concept.title,
        score=correct_count,
        total_questions=total_questions,
        percentage=percentage,
        passed=passed,
        outcome=rec.outcome.value,
        next_concept_id=next_concept_id,
        next_concept_title=next_concept_title,
        can_advance=can_advance,
        questions_detail=questions_detail,
        misconceptions_detected=list(set(misconceptions_detected)),
        weak_concepts=list(rec.evidence_summary.get("prerequisite_gap_signals", {}).keys()),
        ai_guidance=ai_guidance,
        completed_at=datetime.now(timezone.utc).isoformat()
    )


@router.post("/assessments/results/{result_id}/guidance")
@router.get("/assessments/results/{result_id}/guidance")
async def generate_result_guidance(
    result_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
    conn=Depends(get_db_connection)
):
    """Generates and updates Gemini AI personalized guidance for an already saved assessment result."""
    res = crud.get_assessment_result_by_id(conn, result_id)
    if not res:
        # Check if caller passed a concept ID instead of a result ID
        res = crud.get_latest_assessment_result(conn, current_user["id"], result_id.upper())
    if not res:
        raise HTTPException(status_code=404, detail=f"Assessment result '{result_id}' not found.")

    if current_user["id"] != res["learner_id"] and current_user.get("role") != "teacher":
        raise HTTPException(status_code=403, detail="Cannot access assessment result of another learner.")

    questions_detail = res.get("questions_detail", [])
    missed_questions = []
    for qd in questions_detail:
        if not qd.get("is_correct"):
            missed_questions.append({
                "question_id": qd.get("question_id"),
                "prompt": qd.get("prompt"),
                "selected_option_id": qd.get("selected_option_id"),
                "selected_option_text": qd.get("selected_option_text"),
                "correct_option_id": qd.get("correct_option_id"),
                "correct_option_text": qd.get("correct_option_text"),
                "misconception_tag": qd.get("misconception_tag", "none")
            })

    ai_guidance = await generate_assessment_guidance(
        concept_id=res["concept_id"],
        score=res["score"],
        total_questions=res["total_questions"],
        percentage=res["percentage"],
        passed=res["passed"],
        outcome=res["outcome"],
        missed_questions=missed_questions,
        misconceptions=res.get("misconceptions_detected", [])
    )

    crud.update_assessment_result_guidance(conn, res["id"], ai_guidance)
    return ai_guidance


@router.get("/assessments/results/{identifier}", response_model=AssessmentResultResponse)
@router.get("/results/{identifier}", response_model=AssessmentResultResponse)
@router.get("/assessments/{identifier}/result", response_model=AssessmentResultResponse)
def get_assessment_result_unified(
    identifier: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
    conn=Depends(get_db_connection)
):
    """
    Unified retrieval for assessment results.
    Accepts:
    1. Result ID: 'res-...'
    2. Session ID: 'sess-...'
    3. Concept ID: 'MATH-C01', 'MATH-C04', etc.
    Enforces learner ownership and returns structured 404 if not found.
    """
    learner_id = current_user["id"]
    res = None

    if identifier.startswith("res-"):
        res = crud.get_assessment_result_by_id(conn, identifier)
    elif identifier.startswith("sess-"):
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM assessment_results WHERE session_id = ?", (identifier,))
        row = cursor.fetchone()
        if row:
            res = crud.get_assessment_result_by_id(conn, row["id"])
    else:
        # Treat as concept code
        res = crud.get_latest_assessment_result(conn, learner_id, identifier.upper())

    if not res:
        raise HTTPException(
            status_code=404,
            detail=f"No completed assessment result found for identifier '{identifier}'."
        )

    # Ownership check
    if current_user["id"] != res["learner_id"] and current_user.get("role") != "teacher":
        raise HTTPException(status_code=403, detail="Cannot access assessment result of another learner.")

    concept = get_concept(res["concept_id"])
    res["concept_title"] = concept.title if concept else res["concept_id"]
    return AssessmentResultResponse(**res)


@router.get("/assessments/sessions/{session_id}/result", response_model=AssessmentResultResponse)
def get_assessment_result_by_session(
    session_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
    conn=Depends(get_db_connection)
):
    """Retrieves assessment result by session ID, enforcing learner ownership."""
    return get_assessment_result_unified(session_id, current_user, conn)


@router.get("/assessments/results", response_model=List[AssessmentResultResponse])
def list_learner_assessment_results(
    current_user: Dict[str, Any] = Depends(get_current_user),
    conn=Depends(get_db_connection)
):
    """Lists all assessment results for the current authenticated learner."""
    learner_id = current_user["id"]
    rows = crud.get_learner_assessment_results(conn, learner_id)
    output = []
    for r in rows:
        concept = get_concept(r["concept_id"])
        r["concept_title"] = concept.title if concept else r["concept_id"]
        output.append(AssessmentResultResponse(**r))
    return output
