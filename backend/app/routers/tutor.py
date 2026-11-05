"""
SUTRA LEARN — Student AI Tutor Router
Provides natural language mathematical guidance, step-by-step Socratic walkthroughs,
progressive hints, worked examples, and check-my-work capabilities.
Ownership is strictly enforced; students can never access other learners' conversations.
"""

import os
import uuid
import json
import logging
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException, Depends, Header, Request
from pydantic import BaseModel, Field

from app.db.database import get_db_connection
from app.db import crud
from app.auth import get_current_user
from app.auth_rate_limit import ai_rate_limiter
from app.ai.provider import get_ai_provider
from app.ai.curriculum_context import get_learner_context
from app.services.audit import record_audit_event, AuditCategory


router = APIRouter(prefix="/api/v1/tutor", tags=["Student AI Tutor"])
logger = logging.getLogger("sutra.tutor")


class CreateSessionRequest(BaseModel):
    concept_id: Optional[str] = Field(None, description="Anchored concept ID (e.g. MATH-C01)")
    title: Optional[str] = Field(None, description="Optional custom session title")


class TutorChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000, description="Student mathematical question or step")
    conversation_id: Optional[str] = Field(None, description="Existing conversation ID to continue")
    concept_id: Optional[str] = Field(None, description="Anchored concept ID (e.g. MATH-C01)")
    mode: str = Field("guided_learning", description="guided_learning | explain_concept | worked_example | practice | check_my_work | quick_revision | prerequisite_support")


class TutorChatResponse(BaseModel):
    conversation_id: str
    message_id: str
    answer: str
    explanation: Optional[str] = None
    response: Optional[str] = None
    response_type: str
    hints: List[str]
    concept_id: Optional[str]
    requires_follow_up: bool
    provider_metadata: Dict[str, Any]


@router.post("/chat", response_model=TutorChatResponse)
async def tutor_chat(
    req: TutorChatRequest,
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user),
    conn=Depends(get_db_connection)
):
    """
    Primary endpoint for SUTRA AI student tutoring interactions.
    Enforces conversation ownership and grounds responses in NCERT Class 8 curriculum.
    """
    learner_id = current_user["id"]
    learner_role = current_user["role"]
    corr_id = getattr(request.state, "correlation_id", None) or f"req_{uuid.uuid4().hex[:12]}"
    req_start = datetime.now(timezone.utc)

    # Structured Lifecycle: REQUEST_RECEIVED
    logger.info(json.dumps({
        "lifecycle_event": "REQUEST_RECEIVED",
        "request_id": corr_id,
        "endpoint": "/api/v1/tutor/chat",
        "method": "POST",
        "timestamp_utc": req_start.isoformat()
    }))

    # Structured Lifecycle: AUTHENTICATION_VERIFIED
    logger.info(json.dumps({
        "lifecycle_event": "AUTHENTICATION_VERIFIED",
        "request_id": corr_id,
        "actor_id": learner_id,
        "role": learner_role,
        "timestamp_utc": datetime.now(timezone.utc).isoformat()
    }))

    # Enforce sliding-window rate limit on AI inference
    ai_rate_limiter.check_rate_limit(f"tutor_{learner_id}")

    # Structured Lifecycle: TUTOR_REQUEST_VALIDATED
    logger.info(json.dumps({
        "lifecycle_event": "TUTOR_REQUEST_VALIDATED",
        "request_id": corr_id,
        "concept_id": req.concept_id or "MATH-C01",
        "mode": req.mode,
        "timestamp_utc": datetime.now(timezone.utc).isoformat()
    }))

    # 1. Manage or create conversation
    conv_id = req.conversation_id
    if conv_id:
        existing_conv = crud.get_ai_conversation(conn, conv_id)
        if not existing_conv:
            raise HTTPException(status_code=404, detail="Conversation not found.")
        if existing_conv["owner_id"] != learner_id:
            record_audit_event(
                conn=conn,
                event_category=AuditCategory.SECURITY,
                actor_id=learner_id,
                actor_role=learner_role,
                outcome="REJECTED",
                rationale="Unauthorized cross-student conversation access attempt",
                correlation_id=corr_id,
                details={"target_conv_id": conv_id, "actual_owner": existing_conv["owner_id"]}
            )
            raise HTTPException(status_code=403, detail="Forbidden: You do not own this conversation.")
        # If the existing conversation has a generic default title, update it with student's first message
        current_title = existing_conv.get("title", "")
        if current_title.startswith("New Learning Session") or current_title.startswith("Session on"):
            title_snippet = req.message[:45].strip()
            new_title = f"{title_snippet}..." if len(req.message) > 45 else title_snippet
            crud.update_ai_conversation_title(conn, conv_id, new_title)
    else:
        conv_id = str(uuid.uuid4())
        # Generate informative title from message
        title_snippet = req.message[:45].strip()
        title = f"{title_snippet}..." if len(req.message) > 45 else title_snippet
        crud.create_ai_conversation(
            conn=conn,
            conversation_id=conv_id,
            owner_id=learner_id,
            owner_role=learner_role,
            title=title,
            conversation_type="tutor",
            concept_id=req.concept_id
        )
        record_audit_event(
            conn=conn,
            event_category=AuditCategory.AUTHORIZED,
            actor_id=learner_id,
            actor_role=learner_role,
            learner_id=learner_id,
            concept_id=req.concept_id,
            outcome="RECORDED",
            rationale="New AI tutor conversation created",
            correlation_id=corr_id,
            details={"conversation_id": conv_id, "title": title}
        )

    # 2. Record student's incoming message
    user_msg_id = str(uuid.uuid4())
    crud.add_ai_message(
        conn=conn,
        message_id=user_msg_id,
        conversation_id=conv_id,
        sender_role="user",
        content=req.message.strip(),
        response_type="question",
        concept_id=req.concept_id
    )

    # 3. Retrieve conversation history for context
    history = crud.get_ai_messages(conn, conv_id)
    history_records = [{"sender_role": m["sender_role"], "content": m["content"]} for m in history[:-1]]

    # 4. Retrieve learner's own authorized context
    learner_ctx = get_learner_context(conn, learner_id, req.concept_id)

    # 5. Generate AI response through Multi-Model Provider / Orchestrator
    ai_provider = get_ai_provider()
    raw_resp = await ai_provider.generate_tutor_response(
        message=req.message,
        concept_id=req.concept_id,
        mode=req.mode,
        conversation_history=history_records,
        learner_context=learner_ctx
    )

    meta = {
        "provider": raw_resp.get("provider", "NCERT Curriculum Engine"),
        "model": raw_resp.get("model", "curriculum_fallback"),
        "is_fallback": raw_resp.get("is_fallback", False),
        "fallback_reason": raw_resp.get("fallback_reason"),
        "latency_ms": raw_resp.get("latency_ms", 1.0),
        "tokens_used": raw_resp.get("tokens_used"),
        "validation_status": raw_resp.get("validation_status", "CURRICULUM_VERIFIED")
    }

    # 6. Record assistant's response in DB
    assistant_msg_id = str(uuid.uuid4())
    crud.add_ai_message(
        conn=conn,
        message_id=assistant_msg_id,
        conversation_id=conv_id,
        sender_role="assistant",
        content=raw_resp["answer"],
        response_type=raw_resp.get("response_type", "guided_explanation"),
        hints=raw_resp.get("hints", []),
        concept_id=raw_resp.get("concept_id", req.concept_id),
        requires_follow_up=raw_resp.get("requires_follow_up", False),
        provider_metadata=meta
    )

    # Structured Lifecycle: CONVERSATION_PERSISTED
    logger.info(json.dumps({
        "lifecycle_event": "CONVERSATION_PERSISTED",
        "request_id": corr_id,
        "session_id": conv_id,
        "message_id": assistant_msg_id,
        "timestamp_utc": datetime.now(timezone.utc).isoformat()
    }))

    duration_ms = round((datetime.now(timezone.utc) - req_start).total_seconds() * 1000, 2)

    structured_audit_details = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "request_id": corr_id,
        "session_id": conv_id,
        "endpoint": "/api/v1/tutor/chat",
        "operation": "generateContent",
        "model": meta["model"],
        "provider": meta["provider"],
        "environment": os.getenv("APP_ENV", "development"),
        "duration_ms": duration_ms,
        "http_status": 200,
        "outcome": "SUCCESS",
        "error_class": meta.get("fallback_reason") if meta["is_fallback"] else None,
        "retry_count": raw_resp.get("retry_count", 0),
        "tokens_used": meta["tokens_used"]
    }

    record_audit_event(
        conn=conn,
        event_category=AuditCategory.AUTHORIZED,
        actor_id=learner_id,
        actor_role=learner_role,
        learner_id=learner_id,
        concept_id=req.concept_id,
        outcome="RECORDED",
        rationale=f"AI Tutor response generated via {meta['provider']} ({meta['model']})",
        correlation_id=corr_id,
        details=structured_audit_details
    )

    # Structured Lifecycle: RESPONSE_DELIVERED
    logger.info(json.dumps({
        "lifecycle_event": "RESPONSE_DELIVERED",
        "request_id": corr_id,
        "session_id": conv_id,
        "duration_ms": duration_ms,
        "timestamp_utc": datetime.now(timezone.utc).isoformat()
    }))

    ans_text = raw_resp["answer"]
    return TutorChatResponse(
        conversation_id=conv_id,
        message_id=assistant_msg_id,
        answer=ans_text,
        explanation=ans_text,
        response=ans_text,
        response_type=raw_resp.get("response_type", "guided_explanation"),
        hints=raw_resp.get("hints", []),
        concept_id=raw_resp.get("concept_id", req.concept_id),
        requires_follow_up=raw_resp.get("requires_follow_up", False),
        provider_metadata=meta
    )


@router.post("/sessions", status_code=201)
@router.post("/conversations", status_code=201)
async def create_session(
    req: CreateSessionRequest,
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user),
    conn=Depends(get_db_connection)
):
    """
    Creates a new persistent AI tutor conversation session for the authenticated learner.
    Commits immediately to the database and returns the durable session record.
    """
    learner_id = current_user["id"]
    learner_role = current_user["role"]
    corr_id = getattr(request.state, "correlation_id", None) or f"req_{uuid.uuid4().hex[:12]}"
    req_start = datetime.now(timezone.utc)

    conv_id = str(uuid.uuid4())
    default_title = req.title.strip() if req.title and req.title.strip() else (
        f"Session on {req.concept_id}" if req.concept_id else "New Learning Session"
    )

    created_record = crud.create_ai_conversation(
        conn=conn,
        conversation_id=conv_id,
        owner_id=learner_id,
        owner_role=learner_role,
        title=default_title,
        conversation_type="tutor",
        concept_id=req.concept_id
    )

    duration_ms = round((datetime.now(timezone.utc) - req_start).total_seconds() * 1000, 2)

    record_audit_event(
        conn=conn,
        event_category=AuditCategory.AUTHORIZED,
        actor_id=learner_id,
        actor_role=learner_role,
        learner_id=learner_id,
        concept_id=req.concept_id,
        outcome="RECORDED",
        rationale="New AI tutor conversation session created",
        correlation_id=corr_id,
        details={
            "operation": "create_session",
            "session_id": conv_id,
            "title": default_title,
            "concept_id": req.concept_id,
            "duration_ms": duration_ms
        }
    )

    logger.info(json.dumps({
        "lifecycle_event": "SESSION_CREATED",
        "request_id": corr_id,
        "session_id": conv_id,
        "actor_id": learner_id,
        "timestamp_utc": datetime.now(timezone.utc).isoformat()
    }))

    return {
        **created_record,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "messages": []
    }


@router.get("/sessions", response_model=List[Dict[str, Any]])
@router.get("/conversations", response_model=List[Dict[str, Any]])
def list_sessions(
    request: Request = None,
    current_user: Dict[str, Any] = Depends(get_current_user),
    conn=Depends(get_db_connection)
):
    """Lists the authenticated user's own tutor conversations with strict owner isolation."""
    learner_id = current_user["id"]
    return crud.get_user_ai_conversations(conn, owner_id=learner_id, conversation_type="tutor")


@router.get("/sessions/{session_id}")
@router.get("/conversations/{session_id}")
def get_session_detail(
    session_id: str,
    request: Request = None,
    current_user: Dict[str, Any] = Depends(get_current_user),
    conn=Depends(get_db_connection)
):
    """
    Retrieves full conversation messages.
    Strictly verifies ownership; cross-student conversation access is rejected.
    """
    learner_id = current_user["id"]
    learner_role = current_user["role"]
    corr_id = getattr(request.state, "correlation_id", None) if request and hasattr(request, "state") else f"req_{uuid.uuid4().hex[:12]}"

    conv = crud.get_ai_conversation(conn, session_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found.")
    if conv["owner_id"] != learner_id:
        record_audit_event(
            conn=conn,
            event_category=AuditCategory.SECURITY,
            actor_id=learner_id,
            actor_role=learner_role,
            outcome="REJECTED",
            rationale="Cross-student conversation retrieval attempt",
            correlation_id=corr_id,
            details={"target_session_id": session_id}
        )
        raise HTTPException(status_code=403, detail="Forbidden: You cannot access another learner's conversation.")

    messages = crud.get_ai_messages(conn, session_id)
    return {
        "conversation": conv,
        "messages": messages
    }


@router.post("/sessions/{session_id}/reset")
@router.post("/conversations/{session_id}/reset")
def reset_session(
    session_id: str,
    request: Request = None,
    current_user: Dict[str, Any] = Depends(get_current_user),
    conn=Depends(get_db_connection)
):
    """
    Resets the active conversation by clearing its messages while preserving session continuity.
    Strictly enforces learner ownership.
    """
    learner_id = current_user["id"]
    learner_role = current_user["role"]
    corr_id = getattr(request.state, "correlation_id", None) if request and hasattr(request, "state") else f"req_{uuid.uuid4().hex[:12]}"

    conv = crud.get_ai_conversation(conn, session_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found.")
    if conv["owner_id"] != learner_id:
        record_audit_event(
            conn=conn,
            event_category=AuditCategory.SECURITY,
            actor_id=learner_id,
            actor_role=learner_role,
            outcome="REJECTED",
            rationale="Cross-student conversation reset attempt",
            correlation_id=corr_id,
            details={"target_session_id": session_id}
        )
        raise HTTPException(status_code=403, detail="Forbidden: You cannot reset another learner's conversation.")

    deleted_count = crud.clear_ai_conversation_messages(conn, session_id)

    record_audit_event(
        conn=conn,
        event_category=AuditCategory.AUTHORIZED,
        actor_id=learner_id,
        actor_role=learner_role,
        learner_id=learner_id,
        concept_id=conv.get("concept_id"),
        outcome="RECORDED",
        rationale="AI tutor conversation messages cleared and restarted",
        correlation_id=corr_id,
        details={
            "operation": "reset_session",
            "session_id": session_id,
            "cleared_messages_count": deleted_count
        }
    )

    logger.info(json.dumps({
        "lifecycle_event": "SESSION_RESET",
        "request_id": corr_id,
        "session_id": session_id,
        "cleared_messages_count": deleted_count,
        "timestamp_utc": datetime.now(timezone.utc).isoformat()
    }))

    return {
        "status": "success",
        "conversation_id": session_id,
        "cleared_messages_count": deleted_count
    }


@router.delete("/sessions/{session_id}")
@router.delete("/conversations/{session_id}")
def delete_session(
    session_id: str,
    request: Request = None,
    current_user: Dict[str, Any] = Depends(get_current_user),
    conn=Depends(get_db_connection)
):
    """Deletes a conversation owned by the authenticated learner."""
    learner_id = current_user["id"]
    learner_role = current_user["role"]
    corr_id = getattr(request.state, "correlation_id", None) if request and hasattr(request, "state") else f"req_{uuid.uuid4().hex[:12]}"

    conv = crud.get_ai_conversation(conn, session_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found.")
    if conv["owner_id"] != learner_id:
        record_audit_event(
            conn=conn,
            event_category=AuditCategory.SECURITY,
            actor_id=learner_id,
            actor_role=learner_role,
            outcome="REJECTED",
            rationale="Cross-student conversation deletion attempt",
            correlation_id=corr_id,
            details={"target_session_id": session_id}
        )
        raise HTTPException(status_code=403, detail="Forbidden: You cannot delete another learner's conversation.")

    success = crud.delete_ai_conversation(conn, session_id, learner_id)

    record_audit_event(
        conn=conn,
        event_category=AuditCategory.AUTHORIZED,
        actor_id=learner_id,
        actor_role=learner_role,
        learner_id=learner_id,
        concept_id=conv.get("concept_id"),
        outcome="RECORDED",
        rationale="AI tutor conversation deleted",
        correlation_id=corr_id,
        details={
            "operation": "delete_session",
            "session_id": session_id,
            "deleted": success
        }
    )

    return {"status": "success", "deleted": success}


# Backwards compatibility function aliases for existing scripts and callers
list_conversations = list_sessions
get_conversation_detail = get_session_detail
delete_conversation = delete_session

