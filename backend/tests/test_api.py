"""
End-to-end Integration and Security Tests for SUTRA LEARN API.
Tests endpoints, idempotency, adaptive evaluation, teacher overrides,
and server-enforced cryptographic Bearer token authorization.
"""

import os
import uuid
import pytest
from fastapi.testclient import TestClient

test_db_path = "test_sutra_learn.db"
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


def teacher_headers(teacher_id: str = "teacher-01") -> dict:
    token = create_access_token(teacher_id, "teacher", f"Teacher {teacher_id}")
    return {"Authorization": f"Bearer {token}"}


def test_health_and_info(client):
    r1 = client.get("/api/v1/health")
    assert r1.status_code == 200
    assert r1.json()["status"] == "healthy"

    r2 = client.get("/api/v1")
    assert r2.status_code == 200
    assert "SUTRA LEARN" in r2.json()["name"]
    assert "CONFIRM" in r2.json()["learning_paths"]


def test_curriculum_endpoints(client):
    r = client.get("/api/v1/concepts", headers=student_headers("student-01"))
    assert r.status_code == 200
    data = r.json()
    assert len(data["concepts"]) == 6
    assert "prerequisite_graph" in data

    # Detail check
    r_detail = client.get("/api/v1/concepts/MATH-C01")
    assert r_detail.status_code == 200
    assert r_detail.json()["code"] == "INT_ARITH"
    assert len(r_detail.json()["lesson"]["worked_steps"]) >= 2

    # Questions check
    r_q = client.get("/api/v1/concepts/MATH-C01/questions")
    assert r_q.status_code == 200
    questions = r_q.json()
    assert len(questions) >= 5
    assert "prompt" in questions[0]
    assert "hint" in questions[0]


def test_idempotent_attempt_submission(client):
    attempt_id = str(uuid.uuid4())
    learner_id = "student-01"
    headers = student_headers(learner_id)
    payload = {
        "attempt_id": attempt_id,
        "learner_id": learner_id,
        "question_id": "Q-INT-001",
        "concept_id": "MATH-C01",
        "selected_option_id": "A",
        "hint_used": False
    }

    # First attempt
    res1 = client.post("/api/v1/attempts", json=payload, headers=headers)
    assert res1.status_code == 200
    data1 = res1.json()
    assert data1["is_correct"] is True
    assert data1["is_duplicate"] is False

    # Second attempt with same attempt_id (network retry simulation)
    res2 = client.post("/api/v1/attempts", json=payload, headers=headers)
    assert res2.status_code == 200
    data2 = res2.json()
    assert data2["is_duplicate"] is True
    assert "already recorded" in data2["message"]


def test_misconception_distractor_feedback(client):
    attempt_id = str(uuid.uuid4())
    learner_id = "student-02"
    headers = student_headers(learner_id)
    payload = {
        "attempt_id": attempt_id,
        "learner_id": learner_id,
        "question_id": "Q-INT-001",
        "concept_id": "MATH-C01",
        "selected_option_id": "B",  # Distractor with SIGN_ERROR
        "hint_used": False
    }
    res = client.post("/api/v1/attempts", json=payload, headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data["is_correct"] is False
    assert data["misconception_tag"] == "sign_error"
    assert data["misconception_explanation"] is not None
    assert len(data["explanation"]) > 10


def test_adaptive_evaluation_flow(client):
    learner_id = "student-03"
    headers = student_headers(learner_id)

    # Submit first unassisted correct answer on Q-INT-001
    client.post("/api/v1/attempts", json={
        "attempt_id": str(uuid.uuid4()),
        "learner_id": learner_id,
        "question_id": "Q-INT-001",
        "concept_id": "MATH-C01",
        "selected_option_id": "A",
        "hint_used": False
    }, headers=headers)

    # Submit second distinct unassisted correct answer on Q-INT-002
    client.post("/api/v1/attempts", json={
        "attempt_id": str(uuid.uuid4()),
        "learner_id": learner_id,
        "question_id": "Q-INT-002",
        "concept_id": "MATH-C01",
        "selected_option_id": "C",
        "hint_used": False
    }, headers=headers)

    # Evaluate concept
    eval_res = client.post(
        "/api/v1/recommendations/evaluate",
        json={"learner_id": learner_id, "concept_id": "MATH-C01"},
        headers=headers
    )
    assert eval_res.status_code == 200
    rec = eval_res.json()
    assert rec["outcome"] == "STRETCH"
    assert rec["reason_code"] == "STRETCH_MASTERY_DEMONSTRATED"
    assert rec["confidence_score"] >= 0.90

    # Verify progress recorded in learner progress endpoint
    prog_res = client.get(
        f"/api/v1/learners/{learner_id}/progress",
        headers=headers
    )
    assert prog_res.status_code == 200
    prog_list = prog_res.json()["progress"]
    c01_prog = next((p for p in prog_list if p["concept_id"] == "MATH-C01"), None)
    assert c01_prog is not None
    assert c01_prog["status"] == "mastered"


def test_teacher_endpoint_security_and_authorization(client):
    target_student = "student-01"

    # 1. Missing header returns 401
    r_no_header = client.get("/api/v1/teacher/cohort")
    assert r_no_header.status_code == 401

    # 2. Forged spoofed header (x-teacher-id: teacher-01) without Bearer token returns 401 Unauthorized
    r_spoofed_header = client.get(
        "/api/v1/teacher/cohort",
        headers={"x-teacher-id": "teacher-01"}
    )
    assert r_spoofed_header.status_code == 401

    # 3. Student token attempting to access teacher cohort returns 403 Forbidden
    r_student_token = client.get(
        "/api/v1/teacher/cohort",
        headers=student_headers(target_student)
    )
    assert r_student_token.status_code == 403

    # 4. Student attempting teacher override returns 403 Forbidden
    forbidden_payload = {
        "learner_id": target_student,
        "concept_id": "MATH-C01",
        "previous_outcome": "STRETCH",
        "overridden_outcome": "SCAFFOLD",
        "reason": "Student requested extra revision",
        "teacher_id": target_student
    }
    r_forbid = client.post(
        "/api/v1/teacher/override",
        json=forbidden_payload,
        headers=student_headers(target_student)
    )
    assert r_forbid.status_code == 403

    # 5. Teacher with too short reason (< 5 chars) returns 400
    bad_reason_payload = {
        "learner_id": target_student,
        "concept_id": "MATH-C01",
        "previous_outcome": "STRETCH",
        "overridden_outcome": "SCAFFOLD",
        "reason": "bad",
        "teacher_id": "teacher-01"
    }
    r_bad = client.post(
        "/api/v1/teacher/override",
        json=bad_reason_payload,
        headers=teacher_headers("teacher-01")
    )
    assert r_bad.status_code == 400

    # 6. Authorized teacher with valid reason succeeds
    valid_payload = {
        "learner_id": target_student,
        "concept_id": "MATH-C01",
        "previous_outcome": "STRETCH",
        "overridden_outcome": "SCAFFOLD",
        "reason": "Teacher clinical observation: Student hesitated on mental negative addition.",
        "teacher_id": "teacher-01"
    }
    r_ok = client.post(
        "/api/v1/teacher/override",
        json=valid_payload,
        headers=teacher_headers("teacher-01")
    )
    assert r_ok.status_code == 200
    assert r_ok.json()["status"] == "success"

    # 7. Verify audit log recorded intervention
    audit_res = client.get("/api/v1/teacher/overrides", headers=teacher_headers("teacher-01"))
    assert audit_res.status_code == 200
    overrides = audit_res.json()
    assert len(overrides) >= 1
    assert any(o["reason"] == valid_payload["reason"] for o in overrides)

    # 8. Teacher concept difficulty analytics endpoint
    analytics_res = client.get("/api/v1/teacher/analytics/concepts", headers=teacher_headers("teacher-01"))
    assert analytics_res.status_code == 200
    assert isinstance(analytics_res.json(), list)


def test_learner_resource_ownership_protection(client):
    # 1. Requesting attempts without header returns 401
    r_no_header = client.get("/api/v1/learners/student-01/attempts")
    assert r_no_header.status_code == 401

    # 2. Student-02 token attempting to inspect Student-01's attempts returns 403 Forbidden
    r_forbidden = client.get(
        "/api/v1/learners/student-01/attempts",
        headers=student_headers("student-02")
    )
    assert r_forbidden.status_code == 403

    # 3. Student-01 inspecting their own attempts succeeds
    r_own = client.get(
        "/api/v1/learners/student-01/attempts",
        headers=student_headers("student-01")
    )
    assert r_own.status_code == 200
    assert "attempts" in r_own.json()

    # 4. Teacher-01 inspecting Student-01's attempts succeeds
    r_teacher = client.get(
        "/api/v1/learners/student-01/attempts",
        headers=teacher_headers("teacher-01")
    )
    assert r_teacher.status_code == 200
    assert "attempts" in r_teacher.json()


def test_session_auth_endpoint(client):
    """Verifies that the /session endpoint issues real verifiable tokens for known personas."""
    res = client.post("/api/v1/auth/session", json={"learner_id": "student-01"})
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["token_type"] == "Bearer"
    assert data["user_id"] == "student-01"

    # Token can be used to call /me
    me_res = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {data['access_token']}"})
    assert me_res.status_code == 200
    assert me_res.json()["id"] == "student-01"
    assert me_res.json()["role"] == "student"

    # Non-existent learner fails with 404
    bad_res = client.post("/api/v1/auth/session", json={"learner_id": "ghost-student"})
    assert bad_res.status_code == 404


def test_cohort_accuracy_integrity_and_categorized_audit(client):
    """
    Regression test ensuring cohort accuracy never exceeds 100%,
    total_correct <= total_attempts, and categorized audit endpoint returns valid structures.
    """
    cohort_res = client.get("/api/v1/teacher/cohort", headers=teacher_headers("teacher-01"))
    assert cohort_res.status_code == 200
    cohort_data = cohort_res.json()
    assert len(cohort_data) > 0
    for student in cohort_data:
        tot = student["total_attempts"]
        corr = student["total_correct"]
        assert corr <= tot, f"Data integrity violation: total_correct ({corr}) exceeds total_attempts ({tot})"
        if tot > 0:
            acc = student.get("accuracy_percentage")
            assert acc is not None and 0.0 <= acc <= 100.0, f"Accuracy percentage out of bounds: {acc}"

    # Test categorized audit trail
    audit_res = client.get("/api/v1/teacher/audit", headers=teacher_headers("teacher-01"))
    assert audit_res.status_code == 200
    assert isinstance(audit_res.json(), list)

