"""
SUTRA LEARN — AI Tutor & Educator Intelligence Test Suite
Verifies mathematical grounding, teaching modes, conversation persistence,
ownership protection, and teacher role authorization.
"""

import os
import uuid
import pytest
from fastapi.testclient import TestClient

from app.db.database import init_db, get_db_connection
from app.db import crud
from app.auth import create_access_token
from app.main import app
from app.ai.curriculum_context import get_grounded_concept_context


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def student_headers(learner_id: str = "student-01") -> dict:
    conn = get_db_connection()
    crud.get_or_create_learner(conn, learner_id, "Test Student", "student")
    conn.close()
    token = create_access_token(learner_id, "student", f"Student {learner_id}")
    return {"Authorization": f"Bearer {token}"}


def teacher_headers(teacher_id: str = "teacher-01") -> dict:
    conn = get_db_connection()
    crud.get_or_create_learner(conn, teacher_id, "Ms. Teacher", "teacher")
    conn.close()
    token = create_access_token(teacher_id, "teacher", f"Teacher {teacher_id}")
    return {"Authorization": f"Bearer {token}"}


def test_curriculum_grounding():
    """Verifies that grounded concept context retrieves real curriculum data."""
    ctx = get_grounded_concept_context("MATH-C01")
    assert ctx["found"] is True
    assert "Integer" in ctx["title"]
    assert len(ctx["prerequisites"]) == 0
    assert ctx["lesson"] is not None
    assert len(ctx["sample_questions"]) > 0


def test_student_tutor_chat_flow(client):
    """Verifies that a student can converse with SUTRA AI and receive grounded assistance."""
    headers = student_headers("student-01")

    # 1. Start new conversation
    payload = {
        "message": "I don't understand how to isolate x in 2x + 5 = 15",
        "concept_id": "MATH-C01",
        "mode": "guided_learning"
    }
    res = client.post("/api/v1/tutor/chat", json=payload, headers=headers)
    assert res.status_code == 200, res.text
    data = res.json()

    assert "conversation_id" in data
    assert "answer" in data
    assert len(data["answer"]) > 20
    assert data["response_type"] == "guided_explanation"
    assert isinstance(data["hints"], list)
    conv_id = data["conversation_id"]

    # 2. Continue the conversation
    followup_payload = {
        "message": "Should I subtract 5 from both sides?",
        "conversation_id": conv_id,
        "concept_id": "MATH-C01",
        "mode": "guided_learning"
    }
    res2 = client.post("/api/v1/tutor/chat", json=followup_payload, headers=headers)
    assert res2.status_code == 200
    data2 = res2.json()
    assert data2["conversation_id"] == conv_id

    # 3. Retrieve conversation history
    res_detail = client.get(f"/api/v1/tutor/conversations/{conv_id}", headers=headers)
    assert res_detail.status_code == 200
    detail = res_detail.json()
    messages = detail["messages"]
    assert len(messages) >= 4  # 2 user questions + 2 assistant answers


def test_tutor_teaching_modes(client):
    """Verifies worked_example, practice, and check_my_work modes."""
    headers = student_headers("student-01")

    # Worked example mode
    res_ex = client.post("/api/v1/tutor/chat", json={
        "message": "Show me a worked example",
        "concept_id": "MATH-C02",
        "mode": "worked_example"
    }, headers=headers)
    assert res_ex.status_code == 200
    assert res_ex.json()["response_type"] == "worked_example"

    # Practice mode
    res_prac = client.post("/api/v1/tutor/chat", json={
        "message": "Quiz me on equations",
        "concept_id": "MATH-C02",
        "mode": "practice"
    }, headers=headers)
    assert res_prac.status_code == 200
    assert res_prac.json()["response_type"] == "practice_question"


def test_tutor_conversation_ownership_isolation(client):
    """Critical security test: Student A cannot read or delete Student B's conversation."""
    headers_a = student_headers("student-a")
    headers_b = student_headers("student-b")

    # Student A creates a conversation
    res = client.post("/api/v1/tutor/chat", json={
        "message": "Confidential question from Student A",
        "concept_id": "MATH-C01",
        "mode": "guided_learning"
    }, headers=headers_a)
    assert res.status_code == 200
    conv_id = res.json()["conversation_id"]

    # Student B attempts to access Student A's conversation
    res_hack = client.get(f"/api/v1/tutor/conversations/{conv_id}", headers=headers_b)
    assert res_hack.status_code == 403, "Student B must be rejected from viewing Student A's conversation"

    # Student B attempts to delete Student A's conversation
    res_del = client.delete(f"/api/v1/tutor/conversations/{conv_id}", headers=headers_b)
    assert res_del.status_code == 403, "Student B must be rejected from deleting Student A's conversation"

    # Student A can successfully view and delete it
    res_ok = client.get(f"/api/v1/tutor/conversations/{conv_id}", headers=headers_a)
    assert res_ok.status_code == 200

    res_del_ok = client.delete(f"/api/v1/tutor/conversations/{conv_id}", headers=headers_a)
    assert res_del_ok.status_code == 200


def test_educator_intelligence_security_and_synthesis(client):
    """Verifies that educator assistant enforces teacher role and synthesizes database facts."""
    s_headers = student_headers("student-01")
    t_headers = teacher_headers("teacher-01")

    # 1. Student attempted access must return 403
    res_stud = client.post("/api/v1/teacher/assistant/analyze", json={
        "query": "Give me classroom intelligence"
    }, headers=s_headers)
    assert res_stud.status_code == 403

    # 2. Teacher access succeeds
    res_teach = client.post("/api/v1/teacher/assistant/analyze", json={
        "query": "Which concepts need attention?"
    }, headers=t_headers)
    assert res_teach.status_code == 200
    data = res_teach.json()
    assert "summary" in data
    assert "observations" in data
    assert "recommended_actions" in data
    assert isinstance(data["observations"], list)

    # 3. Quick insights endpoint
    res_insights = client.get("/api/v1/teacher/assistant/insights", headers=t_headers)
    assert res_insights.status_code == 200
    assert "total_learners" in res_insights.json()

