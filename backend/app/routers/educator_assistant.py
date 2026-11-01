"""
SUTRA LEARN — Educator Intelligence Router
Provides evidence-grounded classroom analytics, concept difficulty identification,
and teacher-approved intervention recommendations.
Enforces verified teacher authorization.
"""

import uuid
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field

from app.db.database import get_db_connection
from app.db import crud
from app.auth import require_teacher
from app.ai.provider import get_ai_provider


router = APIRouter(prefix="/api/v1/teacher/assistant", tags=["Educator Intelligence"])


class EducatorAnalysisRequest(BaseModel):
    query: str = Field(min_length=1, max_length=2000, description="Pedagogical inquiry or classroom diagnostic question")
    specific_learner_id: Optional[str] = Field(None, description="Optional target learner ID for focused dossier")
    conversation_id: Optional[str] = Field(None, description="Optional existing conversation ID")


class EducatorAnalysisResponse(BaseModel):
    conversation_id: str
    message_id: str
    summary: str
    observations: List[str]
    recommended_actions: List[str]
    struggling_learner_count: int
    low_accuracy_concepts: List[str]
    provider_metadata: Dict[str, Any]


@router.post("/analyze", response_model=EducatorAnalysisResponse)
async def analyze_classroom(
    req: EducatorAnalysisRequest,
    current_teacher: Dict[str, Any] = Depends(require_teacher),
    conn=Depends(get_db_connection)
):
    """
    Synthesizes real classroom performance and identifies prerequisite bottlenecks.
    Strictly protected by verified teacher token; student callers receive 403.
    """
    teacher_id = current_teacher["id"]

    # 1. Fetch verified database evidence
    cohort = crud.get_teacher_cohort_summary(conn)
    concept_analytics = crud.get_teacher_concept_analytics(conn)

    # 2. Manage or create conversation
    conv_id = req.conversation_id
    if conv_id:
        existing_conv = crud.get_ai_conversation(conn, conv_id)
        if not existing_conv or existing_conv["owner_id"] != teacher_id:
            conv_id = str(uuid.uuid4())
    else:
        conv_id = str(uuid.uuid4())
        title_snippet = req.query[:45].strip()
        title = f"Classroom: {title_snippet}..." if len(req.query) > 45 else f"Classroom: {title_snippet}"
        crud.create_ai_conversation(
            conn=conn,
            conversation_id=conv_id,
            owner_id=teacher_id,
            owner_role="teacher",
            title=title,
            conversation_type="educator_assistant"
        )

    # Record teacher message
    user_msg_id = str(uuid.uuid4())
    crud.add_ai_message(
        conn=conn,
        message_id=user_msg_id,
        conversation_id=conv_id,
        sender_role="user",
        content=req.query.strip(),
        response_type="inquiry"
    )

    # 3. Generate evidence-grounded AI analysis
    provider = get_ai_provider()
    analysis = await provider.generate_educator_insight(
        query=req.query,
        cohort_summary=cohort,
        concept_analytics=concept_analytics,
        specific_learner_id=req.specific_learner_id
    )

    # 4. Record assistant message
    asst_msg_id = str(uuid.uuid4())
    crud.add_ai_message(
        conn=conn,
        message_id=asst_msg_id,
        conversation_id=conv_id,
        sender_role="assistant",
        content=analysis["summary"],
        response_type="educator_summary",
        provider_metadata={
            "provider": analysis.get("provider"),
            "model": analysis.get("model"),
            "is_fallback": analysis.get("is_fallback", False)
        }
    )

    return EducatorAnalysisResponse(
        conversation_id=conv_id,
        message_id=asst_msg_id,
        summary=analysis["summary"],
        observations=analysis.get("observations", []),
        recommended_actions=analysis.get("recommended_actions", []),
        struggling_learner_count=analysis.get("struggling_learner_count", 0),
        low_accuracy_concepts=analysis.get("low_accuracy_concepts", []),
        provider_metadata={
            "provider": analysis.get("provider"),
            "model": analysis.get("model"),
            "is_fallback": analysis.get("is_fallback", False)
        }
    )


@router.get("/insights")
def get_quick_insights(
    current_teacher: Dict[str, Any] = Depends(require_teacher),
    conn=Depends(get_db_connection)
):
    """Returns quick cohort highlights and friction points for the Educator Workspace."""
    cohort = crud.get_teacher_cohort_summary(conn)
    concept_analytics = crud.get_teacher_concept_analytics(conn)

    struggling = [s for s in cohort if s.get("needs_review") or (s.get("accuracy_percentage") is not None and s.get("accuracy_percentage") < 65.0)]
    low_concepts = [c for c in concept_analytics if c.get("accuracy_percentage", 0.0) < 70.0]

    return {
        "total_learners": len(cohort),
        "struggling_learner_count": len(struggling),
        "low_accuracy_concept_count": len(low_concepts),
        "low_accuracy_concepts": low_concepts,
        "struggling_learners": struggling
    }

