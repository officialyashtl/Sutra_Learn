"""
SUTRA LEARN — Student AI Tutor Router
Provides natural language mathematical guidance, step-by-step Socratic walkthroughs,
progressive hints, worked examples, and check-my-work capabilities.
Ownership is strictly enforced; students can never access other learners' conversations.
"""

import uuid
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel, Field

from app.db.database import get_db_connection
from app.db import crud
from app.auth import get_current_user
from app.ai.provider import get_ai_provider
from app.ai.curriculum_context import get_learner_context


router = APIRouter(prefix="/api/v1/tutor", tags=["Student AI Tutor"])


class TutorChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000, description="Student mathematical question or step")
    conversation_id: Optional[str] = Field(None, description="Existing conversation ID to continue")
    concept_id: Optional[str] = Field(None, description="Anchored concept ID (e.g. MATH-C01)")
    mode: str = Field("guided_learning", description="guided_learning | explain_concept | worked_example | practice | check_my_work | quick_revision | prerequisite_support")


class TutorChatResponse(BaseModel):
    conversation_id: str
    message_id: str
    answer: str
    response_type: str
    hints: List[str]
    concept_id: Optional[str]
    requires_follow_up: bool
    provider_metadata: Dict[str, Any]


@router.post("/chat", response_model=TutorChatResponse)
async def tutor_chat(
    req: TutorChatRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    conn=Depends(get_db_connection)
):
    """
    Primary endpoint for SUTRA AI student tutoring interactions.
    Enforces conversation ownership and grounds responses in NCERT Class 8 curriculum.
    """
    learner_id = current_user["id"]
    learner_role = current_user["role"]

    # 1. Manage or create conversation
    conv_id = req.conversation_id
    if conv_id:
        existing_conv = crud.get_ai_conversation(conn, conv_id)
        if not existing_conv:
            raise HTTPException(status_code=404, detail="Conversation not found.")
        if existing_conv["owner_id"] != learner_id:
            raise HTTPException(status_code=403, detail="Forbidden: You do not own this conversation.")
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

    # 5. Generate AI response
    provider = get_ai_provider()
    tutor_res = await provider.generate_tutor_response(
        message=req.message,
        concept_id=req.concept_id,
        mode=req.mode,
        conversation_history=history_records,
        learner_context=learner_ctx
    )

    # 6. Record assistant's response in DB
    assistant_msg_id = str(uuid.uuid4())
    crud.add_ai_message(
        conn=conn,
        message_id=assistant_msg_id,
        conversation_id=conv_id,
        sender_role="assistant",
        content=tutor_res["answer"],
        response_type=tutor_res.get("response_type", "guided_explanation"),
        hints=tutor_res.get("hints", []),
        concept_id=tutor_res.get("concept_id"),
        requires_follow_up=tutor_res.get("requires_follow_up", False),
        provider_metadata={
            "provider": tutor_res.get("provider"),
            "model": tutor_res.get("model"),
            "is_fallback": tutor_res.get("is_fallback", False),
            "fallback_reason": tutor_res.get("fallback_reason")
        }
    )

    return TutorChatResponse(
        conversation_id=conv_id,
        message_id=assistant_msg_id,
        answer=tutor_res["answer"],
        response_type=tutor_res.get("response_type", "guided_explanation"),
        hints=tutor_res.get("hints", []),
        concept_id=tutor_res.get("concept_id"),
        requires_follow_up=tutor_res.get("requires_follow_up", False),
        provider_metadata={
            "provider": tutor_res.get("provider"),
            "model": tutor_res.get("model"),
            "is_fallback": tutor_res.get("is_fallback", False),
            "fallback_reason": tutor_res.get("fallback_reason")
        }
    )


@router.get("/conversations", response_model=List[Dict[str, Any]])
def list_conversations(
    current_user: Dict[str, Any] = Depends(get_current_user),
    conn=Depends(get_db_connection)
):
    """Lists the authenticated user's own tutor conversations."""
    return crud.get_user_ai_conversations(conn, owner_id=current_user["id"], conversation_type="tutor")


@router.get("/conversations/{conversation_id}")
def get_conversation_detail(
    conversation_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
    conn=Depends(get_db_connection)
):
    """
    Retrieves full conversation messages.
    Strictly verifies ownership; cross-student conversation access is rejected.
    """
    conv = crud.get_ai_conversation(conn, conversation_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found.")
    if conv["owner_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Forbidden: You cannot access another learner's conversation.")

    messages = crud.get_ai_messages(conn, conversation_id)
    return {
        "conversation": conv,
        "messages": messages
    }


@router.delete("/conversations/{conversation_id}")
def delete_conversation(
    conversation_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
    conn=Depends(get_db_connection)
):
    """Deletes a conversation owned by the authenticated learner."""
    conv = crud.get_ai_conversation(conn, conversation_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found.")
    if conv["owner_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Forbidden: You cannot delete another learner's conversation.")

    success = crud.delete_ai_conversation(conn, conversation_id, current_user["id"])
    return {"status": "success", "deleted": success}

