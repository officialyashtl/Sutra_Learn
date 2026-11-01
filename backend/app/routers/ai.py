"""
SUTRA LEARN — AI Infrastructure & Orchestration Router
Endpoints:
  GET  /api/v1/ai/health      - System-wide AI health, circuit breaker states, and model availability
  GET  /api/v1/ai/providers   - Detailed Provider Registry diagnostics (Authenticated)
  POST /api/v1/ai/tutor       - Direct student tutor orchestration
  POST /api/v1/ai/educator    - Direct educator classroom analytics orchestration
"""

import time
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field

from app.auth import get_current_user, require_teacher
from app.ai.config import get_ai_settings
from app.ai.registry import get_ai_registry
from app.ai.orchestrator import get_ai_orchestrator
from app.ai.provider import get_ai_provider
from app.ai.models import ProviderHealth, AIResponse
from app.db.database import get_db_connection
from app.db import crud

router = APIRouter(prefix="/api/v1/ai", tags=["AI Infrastructure"])


class AIHealthResponse(BaseModel):
    status: str
    operating_mode: str
    offline_mode: bool
    circuit_breakers: Dict[str, Any]
    providers: List[ProviderHealth]
    timestamp: float


class AITutorDirectRequest(BaseModel):
    message: str = Field(min_length=1, max_length=8000)
    concept_id: Optional[str] = None
    mode: str = "guided_learning"
    conversation_id: Optional[str] = None


class AIEducatorDirectRequest(BaseModel):
    query: str = Field(min_length=1, max_length=2000)
    specific_learner_id: Optional[str] = None
    conversation_id: Optional[str] = None


class AIEducatorResponse(BaseModel):
    conversation_id: str
    message_id: str
    summary: str
    observations: List[str]
    recommended_actions: List[str]
    struggling_learner_count: int
    low_accuracy_concepts: List[str]
    provider_metadata: Dict[str, Any]


@router.get("/health", response_model=AIHealthResponse)
async def get_ai_health():
    """
    Returns live health telemetry for all AI providers without exposing secrets.
    Evaluates real-time socket reachability for Ollama and API configuration for Gemini.
    """
    settings = get_ai_settings()
    registry = get_ai_registry()
    providers_health = await registry.evaluate_provider_health()

    cb_status = {
        pid: cb.get_status() for pid, cb in registry.circuit_breakers.items()
    }

    return AIHealthResponse(
        status="healthy",
        operating_mode=settings.ai_mode,
        offline_mode=settings.ai_offline_mode,
        circuit_breakers=cb_status,
        providers=providers_health,
        timestamp=time.time()
    )


@router.get("/providers", response_model=List[ProviderHealth])
async def list_ai_providers(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Returns full Provider Registry diagnostics for authenticated operators.
    """
    registry = get_ai_registry()
    return await registry.evaluate_provider_health()


@router.post("/tutor", response_model=AIResponse)
async def direct_tutor_orchestration(
    req: AITutorDirectRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    conn=Depends(get_db_connection)
):
    """
    Orchestrates student inquiry through the 12-state AI Orchestrator.
    Enforces student ownership and persists conversation history.
    """
    orchestrator = get_ai_orchestrator()
    learner_id = current_user["id"]
    role = current_user.get("role", "student")

    conv_id = req.conversation_id or f"conv_{learner_id}_{req.concept_id or 'gen'}"

    # Verify or create conversation in DB
    existing_conv = crud.get_ai_conversation(conn, conv_id)
    if existing_conv:
        if existing_conv["owner_id"] != learner_id:
            raise HTTPException(status_code=403, detail="Forbidden: You do not own this conversation.")
    else:
        crud.create_ai_conversation(
            conn=conn,
            conversation_id=conv_id,
            owner_id=learner_id,
            owner_role=role,
            title=f"Tutoring: {req.message[:30]}",
            conversation_type="tutor",
            concept_id=req.concept_id
        )

    # Fetch previous messages for context
    history_rows = crud.get_ai_messages(conn, conv_id)
    history = [{"sender_role": m["sender_role"], "content": m["content"]} for m in history_rows[-8:]]

    # Execute through orchestrator
    response = await orchestrator.execute_tutor_request(
        user_id=learner_id,
        role=role,
        message=req.message,
        conversation_id=conv_id,
        concept_id=req.concept_id,
        mode=req.mode,
        conversation_history=history,
        learner_context={"learner_id": learner_id, "conversation_id": conv_id}
    )

    # Persist assistant message in DB
    crud.add_ai_message(
        conn=conn,
        message_id=f"msg_{response.request_id}",
        conversation_id=conv_id,
        sender_role="assistant",
        content=response.answer,
        response_type=response.response_type,
        hints=response.hints,
        concept_id=response.concept_id,
        requires_follow_up=response.requires_follow_up,
        provider_metadata={
            "request_id": response.request_id,
            "provider": response.provider,
            "model": response.model,
            "is_fallback": response.is_fallback,
            "fallback_reason": response.fallback_reason,
            "latency_ms": response.latency_ms,
            "validation_status": response.validation_status
        }
    )

    return response


@router.post("/educator", response_model=AIEducatorResponse)
async def direct_educator_orchestration(
    req: AIEducatorDirectRequest,
    current_teacher: Dict[str, Any] = Depends(require_teacher),
    conn=Depends(get_db_connection)
):
    """
    Direct educator intelligence synthesis for teachers.
    Strictly protected by verified teacher token; student callers receive 403.
    """
    import uuid
    teacher_id = current_teacher["id"]

    cohort = crud.get_teacher_cohort_summary(conn)
    concept_analytics = crud.get_teacher_concept_analytics(conn)

    conv_id = req.conversation_id
    if conv_id:
        existing_conv = crud.get_ai_conversation(conn, conv_id)
        if not existing_conv or existing_conv["owner_id"] != teacher_id:
            conv_id = f"conv_t_{uuid.uuid4().hex[:10]}"
    else:
        conv_id = f"conv_t_{uuid.uuid4().hex[:10]}"
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

    user_msg_id = f"msg_{uuid.uuid4().hex[:12]}"
    crud.add_ai_message(
        conn=conn,
        message_id=user_msg_id,
        conversation_id=conv_id,
        sender_role="user",
        content=req.query.strip(),
        response_type="inquiry"
    )

    provider = get_ai_provider()
    analysis = await provider.generate_educator_insight(
        query=req.query,
        cohort_summary=cohort,
        concept_analytics=concept_analytics,
        specific_learner_id=req.specific_learner_id
    )

    asst_msg_id = f"msg_{uuid.uuid4().hex[:12]}"
    crud.add_ai_message(
        conn=conn,
        message_id=asst_msg_id,
        conversation_id=conv_id,
        sender_role="assistant",
        content=analysis["summary"],
        response_type="classroom_insight",
        provider_metadata={
            "provider": analysis.get("provider", "SutraEducatorIntelligenceEngine"),
            "model": analysis.get("model", "ncert-class8-analytics-v1"),
            "is_fallback": analysis.get("is_fallback", False)
        }
    )

    return AIEducatorResponse(
        conversation_id=conv_id,
        message_id=asst_msg_id,
        summary=analysis["summary"],
        observations=analysis.get("observations", []),
        recommended_actions=analysis.get("recommended_actions", []),
        struggling_learner_count=analysis.get("struggling_learner_count", 0),
        low_accuracy_concepts=analysis.get("low_accuracy_concepts", []),
        provider_metadata={
            "provider": analysis.get("provider", "SutraEducatorIntelligenceEngine"),
            "model": analysis.get("model", "ncert-class8-analytics-v1"),
            "is_fallback": analysis.get("is_fallback", False)
        }
    )
