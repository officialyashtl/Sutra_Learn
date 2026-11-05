"""
Test Assessment Complete, Scoring, Explanations, AI Guidance, Persistence, and Progression.
"""

import os
import uuid
import pytest
from fastapi.testclient import TestClient

test_db_path = "test_assessment_db.db"
os.environ["SUTRA_DB_PATH"] = test_db_path

from app.db.database import init_db
from app.auth import create_access_token
from app.main import app


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    if os.path.exists(test_db_path):
        try:
            os.remove(test_db_path)
        except Exception:
            pass
    init_db(test_db_path)
    yield
    if os.path.exists(test_db_path):
        try:
            os.remove(test_db_path)
        except Exception:
            pass


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def student_headers(learner_id: str = "student-01") -> dict:
    token = create_access_token(learner_id, "student", f"Student {learner_id}")
    return {"Authorization": f"Bearer {token}"}


def test_assessment_unauthorized_rejection(client):
    """Endpoints require valid authentication."""
    r1 = client.post("/api/v1/assessments/complete", json={
        "concept_id": "MATH-C01",
        "submissions": []
    })
    assert r1.status_code == 401

    r2 = client.get("/api/v1/assessments/results/MATH-C01")
    assert r2.status_code == 401


def test_assessment_complete_scoring_and_explanations(client):
    """
    Submits 5 questions for MATH-C01:
    - Q-INT-001: Selected A (Correct)
    - Q-INT-002: Selected B (Incorrect - SIGN_ERROR)
    - Q-INT-003: Selected A (Correct)
    - Q-INT-004: Selected B (Incorrect - DISTRIBUTIVE_SIGN)
    - Q-INT-005: Selected A (Correct)
    Expected: Score 3/5 (60.0%), Passed, Question details populated, AI Guidance present.
    """
    session_id = f"sess-{uuid.uuid4().hex[:8]}"
    payload = {
        "concept_id": "MATH-C01",
        "session_id": session_id,
        "submissions": [
            {"question_id": "Q-INT-001", "selected_option_id": "A"},
            {"question_id": "Q-INT-002", "selected_option_id": "B"},
            {"question_id": "Q-INT-003", "selected_option_id": "A"},
            {"question_id": "Q-INT-004", "selected_option_id": "B"},
            {"question_id": "Q-INT-005", "selected_option_id": "A"},
        ]
    }

    res = client.post(
        "/api/v1/assessments/complete",
        json=payload,
        headers=student_headers("student-01")
    )
    assert res.status_code == 200
    data = res.json()

    assert data["concept_id"] == "MATH-C01"
    assert data["concept_title"] == "Integer Arithmetic"
    assert data["score"] == 3
    assert data["total_questions"] == 5
    assert data["percentage"] == 60.0
    assert data["passed"] is False
    assert len(data["questions_detail"]) == 5

    # Check question 1 (Correct)
    q1 = data["questions_detail"][0]
    assert q1["question_id"] == "Q-INT-001"
    assert q1["is_correct"] is True
    assert q1["selected_option_id"] == "A"
    assert q1["correct_option_id"] == "A"
    assert len(q1["explanation"]) > 0

    # Check question 2 (Incorrect with misconception)
    q2 = data["questions_detail"][1]
    assert q2["question_id"] == "Q-INT-002"
    assert q2["is_correct"] is False
    assert q2["selected_option_id"] == "B"
    assert q2["correct_option_id"] == "C"
    assert q2["misconception_tag"] is not None
    assert len(q2["explanation"]) > 0

    # Check AI Guidance
    guidance = data["ai_guidance"]
    assert "summary" in guidance and len(guidance["summary"]) > 0
    assert "strengths" in guidance and isinstance(guidance["strengths"], list)
    assert "focus_area" in guidance and len(guidance["focus_area"]) > 0
    assert "action_step" in guidance and len(guidance["action_step"]) > 0
    assert "provider" in guidance

    # Test persistence retrieval
    persisted_res = client.get(
        "/api/v1/assessments/results/MATH-C01",
        headers=student_headers("student-01")
    )
    assert persisted_res.status_code == 200
    pdata = persisted_res.json()
    assert pdata["id"] == data["id"]
    assert pdata["score"] == 3
    assert len(pdata["questions_detail"]) == 5

    # Test Idempotency with same session_id
    idemp_res = client.post(
        "/api/v1/assessments/complete",
        json=payload,
        headers=student_headers("student-01")
    )
    assert idemp_res.status_code == 200
    idata = idemp_res.json()
    assert idata["id"] == data["id"]
    assert idata["score"] == 3


def test_assessment_progression_unlocks_next_concept(client):
    """
    Submits 5/5 correct answers for MATH-C01.
    Verifies adaptive outcome is STRETCH and next concept MATH-C02 is unlocked.
    """
    learner_id = "student-02"
    session_id = f"sess-{uuid.uuid4().hex[:8]}"

    payload = {
        "concept_id": "MATH-C01",
        "session_id": session_id,
        "submissions": [
            {"question_id": "Q-INT-001", "selected_option_id": "A"},
            {"question_id": "Q-INT-002", "selected_option_id": "C"},
            {"question_id": "Q-INT-003", "selected_option_id": "A"},
            {"question_id": "Q-INT-004", "selected_option_id": "A"},
            {"question_id": "Q-INT-005", "selected_option_id": "A"},
        ]
    }

    res = client.post(
        "/api/v1/assessments/complete",
        json=payload,
        headers=student_headers(learner_id)
    )
    assert res.status_code == 200
    data = res.json()

    assert data["score"] == 5
    assert data["percentage"] == 100.0
    assert data["passed"] is True
    assert data["outcome"] == "STRETCH"
    assert data["can_advance"] is True
    assert data["next_concept_id"] == "MATH-C02"

    # Verify curriculum concepts endpoint reflects unlocked state
    concepts_res = client.get("/api/v1/concepts", headers=student_headers(learner_id))
    assert concepts_res.status_code == 200
    concepts_list = concepts_res.json()["concepts"]
    math_c02 = next((c for c in concepts_list if c["id"] == "MATH-C02"), None)
    assert math_c02 is not None
    assert math_c02["is_unlocked"] is True
    assert len(math_c02["missing_prerequisites"]) == 0
