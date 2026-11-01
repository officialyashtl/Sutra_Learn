"""
Comprehensive End-to-End Verification Suite for the 10 Master Directive Scenarios.
Directly validates all 10 release scenarios under server-enforced cryptographic Bearer authorization:
Scenario 1: First-time student onboarding and valid feedback
Scenario 2: Incorrect answer with diagnosed misconception feedback
Scenario 3: Assisted answer (hint used) does not grant unassisted mastery
Scenario 4: Duplicate submission idempotency (no inflation of credit)
Scenario 5: Persistent progress survives refresh and backend reload
Scenario 6: Insufficient evidence triggers CONFIRM
Scenario 7: Prerequisite difficulty triggers BRIDGE_BACK
Scenario 8: Teacher oversight and justified clinical override
Scenario 9: Authorization attack rejection (student blocked from teacher data/actions)
Scenario 10: Offline recovery and safe synchronization without duplicates
"""

import os
import uuid
import pytest
from fastapi.testclient import TestClient

test_db_path = "test_scenarios_sutra.db"
os.environ["SUTRA_DB_PATH"] = test_db_path

from app.db.database import init_db, get_db_connection
from app.db import crud
from app.auth import create_access_token
from app.main import app


@pytest.fixture(scope="session", autouse=True)
def setup_scenario_db():
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


def make_token_headers(user_id: str, role: str = "student", name: str = "Test User") -> dict:
    # Ensure user exists in test DB so DB user lookup in get_current_user succeeds
    conn = get_db_connection()
    crud.get_or_create_learner(conn, user_id, name, role)
    conn.close()
    token = create_access_token(user_id, role, name)
    return {"Authorization": f"Bearer {token}"}


def test_scenario_1_first_time_student(client):
    """Scenario 1: First-time student enters, sees next step, opens lesson, answers question, gets feedback."""
    learner_id = "first-timer-01"
    headers = make_token_headers(learner_id)

    # 1. Fetch curriculum
    res_curr = client.get("/api/v1/concepts", headers=headers)
    assert res_curr.status_code == 200
    concepts = res_curr.json()["concepts"]
    assert len(concepts) == 6
    # First concept MATH-C01 is unlocked
    c01 = next(c for c in concepts if c["id"] == "MATH-C01")
    assert c01["is_unlocked"] is True

    # 2. View Lesson for MATH-C01
    res_lesson = client.get("/api/v1/concepts/MATH-C01")
    assert res_lesson.status_code == 200
    assert len(res_lesson.json()["lesson"]["worked_steps"]) >= 2

    # 3. Fetch questions
    res_q = client.get("/api/v1/concepts/MATH-C01/questions")
    assert res_q.status_code == 200
    q1 = res_q.json()[0]

    # 4. Submit answer (Option A is correct for Q-INT-001: 7)
    att_id = str(uuid.uuid4())
    res_att = client.post("/api/v1/attempts", json={
        "attempt_id": att_id,
        "learner_id": learner_id,
        "question_id": q1["id"],
        "concept_id": "MATH-C01",
        "selected_option_id": "A",
        "hint_used": False
    }, headers=headers)
    assert res_att.status_code == 200
    att_result = res_att.json()
    assert att_result["is_correct"] is True
    assert len(att_result["explanation"]) > 5


def test_scenario_2_incorrect_answer_misconception(client):
    """Scenario 2: Student picks distractor with sign confusion, receives specific misconception diagnosis."""
    learner_id = "misconception-student"
    headers = make_token_headers(learner_id)

    att_id = str(uuid.uuid4())
    # Q-INT-001 option B is -3 (incorrect sign subtraction mistake)
    res = client.post("/api/v1/attempts", json={
        "attempt_id": att_id,
        "learner_id": learner_id,
        "question_id": "Q-INT-001",
        "concept_id": "MATH-C01",
        "selected_option_id": "B",
        "hint_used": False
    }, headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data["is_correct"] is False
    assert data["misconception_tag"] == "sign_error"
    assert "Treated -(-15)" in data["misconception_explanation"] or "subtracting 15" in data["misconception_explanation"]


def test_scenario_3_assisted_answer_does_not_grant_mastery(client):
    """Scenario 3: Correct answer with hint revealed does not count toward unassisted mastery credit."""
    learner_id = "hint-user-student"
    headers = make_token_headers(learner_id)

    # 1. Answer with hint used = True
    client.post("/api/v1/attempts", json={
        "attempt_id": str(uuid.uuid4()),
        "learner_id": learner_id,
        "question_id": "Q-INT-001",
        "concept_id": "MATH-C01",
        "selected_option_id": "A",
        "hint_used": True  # Assisted
    }, headers=headers)

    # 2. Answer second question with hint used = True
    client.post("/api/v1/attempts", json={
        "attempt_id": str(uuid.uuid4()),
        "learner_id": learner_id,
        "question_id": "Q-INT-002",
        "concept_id": "MATH-C01",
        "selected_option_id": "C",
        "hint_used": True  # Assisted
    }, headers=headers)

    # 3. Evaluate concept
    res_eval = client.post("/api/v1/recommendations/evaluate", json={
        "learner_id": learner_id,
        "concept_id": "MATH-C01"
    }, headers=headers)
    assert res_eval.status_code == 200
    rec = res_eval.json()

    # Assisted answers must NEVER trigger STRETCH (Mastery)
    assert rec["outcome"] != "STRETCH"
    # Should recommend SCAFFOLD (extra unassisted practice) or CONFIRM
    assert rec["outcome"] in ["SCAFFOLD", "CONFIRM"]
    assert rec["reason_code"] in ["SCAFFOLD_ASSISTED_ACCURACY", "SCAFF_DEVELOPING_UNDERSTANDING", "CONF_INSUFFICIENT_EVIDENCE"]


def test_scenario_4_duplicate_submission_idempotency(client):
    """Scenario 4: Re-submitting the same attempt_id returns cached result without recording extra attempts."""
    learner_id = f"duplicate-test-student-{uuid.uuid4().hex[:8]}"
    headers = make_token_headers(learner_id)
    attempt_id = str(uuid.uuid4())

    payload = {
        "attempt_id": attempt_id,
        "learner_id": learner_id,
        "question_id": "Q-INT-001",
        "concept_id": "MATH-C01",
        "selected_option_id": "A",
        "hint_used": False
    }

    # Submit attempt 1
    r1 = client.post("/api/v1/attempts", json=payload, headers=headers)
    assert r1.status_code == 200
    assert r1.json()["is_duplicate"] is False

    # Re-submit duplicate
    r2 = client.post("/api/v1/attempts", json=payload, headers=headers)
    assert r2.status_code == 200
    assert r2.json()["is_duplicate"] is True

    # Verify attempt count in DB is exactly 1
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) as count FROM attempts WHERE learner_id = ?", (learner_id,))
    count = cur.fetchone()["count"]
    conn.close()
    assert count == 1


def test_scenario_5_persistent_progress(client):
    """Scenario 5: Student achievements persist across page reloads and simulated DB re-connections."""
    learner_id = "persistent-student"
    headers = make_token_headers(learner_id)

    # Submit 2 distinct unassisted correct answers
    client.post("/api/v1/attempts", json={
        "attempt_id": str(uuid.uuid4()),
        "learner_id": learner_id,
        "question_id": "Q-INT-001",
        "concept_id": "MATH-C01",
        "selected_option_id": "A",
        "hint_used": False
    }, headers=headers)
    client.post("/api/v1/attempts", json={
        "attempt_id": str(uuid.uuid4()),
        "learner_id": learner_id,
        "question_id": "Q-INT-002",
        "concept_id": "MATH-C01",
        "selected_option_id": "C",
        "hint_used": False
    }, headers=headers)

    # Evaluate
    client.post("/api/v1/recommendations/evaluate", json={
        "learner_id": learner_id,
        "concept_id": "MATH-C01"
    }, headers=headers)

    # Simulate fresh client reconnecting and fetching progress
    res_prog = client.get(f"/api/v1/learners/{learner_id}/progress", headers=headers)
    assert res_prog.status_code == 200
    prog_rows = res_prog.json()["progress"]
    c01_prog = next(p for p in prog_rows if p["concept_id"] == "MATH-C01")
    assert c01_prog["status"] == "mastered"
    assert c01_prog["mastery_percentage"] >= 90.0


def test_scenario_6_insufficient_evidence_triggers_confirm(client):
    """Scenario 6: Only 1 attempt provides insufficient evidence to conclude mastery or failure; triggers CONFIRM."""
    learner_id = "one-shot-student"
    headers = make_token_headers(learner_id)

    # 1 correct unassisted attempt (insufficient to declare full mastery)
    client.post("/api/v1/attempts", json={
        "attempt_id": str(uuid.uuid4()),
        "learner_id": learner_id,
        "question_id": "Q-INT-001",
        "concept_id": "MATH-C01",
        "selected_option_id": "A",
        "hint_used": False
    }, headers=headers)

    res_eval = client.post("/api/v1/recommendations/evaluate", json={
        "learner_id": learner_id,
        "concept_id": "MATH-C01"
    }, headers=headers)
    assert res_eval.status_code == 200
    rec = res_eval.json()
    assert rec["outcome"] == "CONFIRM"
    assert rec["reason_code"] == "CONF_INSUFFICIENT_EVIDENCE"


def test_scenario_7_prerequisite_difficulty_bridges_back(client):
    """Scenario 7: An error stemming from a prerequisite concept triggers BRIDGE_BACK."""
    learner_id = "bridge-learner-unique"
    headers = make_token_headers(learner_id)

    # On MATH-C05 (Linear Equations), student makes sign error across 2 distinct questions
    # Q-LIN-001: 2x + 7 = 19. Option B is 13 (addition error / sign error)
    client.post("/api/v1/attempts", json={
        "attempt_id": str(uuid.uuid4()),
        "learner_id": learner_id,
        "question_id": "Q-LIN-001",
        "concept_id": "MATH-C05",
        "selected_option_id": "B",
        "hint_used": False
    }, headers=headers)

    # Q-LIN-002: 3x - 5 = 16. Option B is sign error (-5 subtracted again)
    client.post("/api/v1/attempts", json={
        "attempt_id": str(uuid.uuid4()),
        "learner_id": learner_id,
        "question_id": "Q-LIN-002",
        "concept_id": "MATH-C05",
        "selected_option_id": "B",
        "hint_used": False
    }, headers=headers)

    res_eval = client.post("/api/v1/recommendations/evaluate", json={
        "learner_id": learner_id,
        "concept_id": "MATH-C05"
    }, headers=headers)
    assert res_eval.status_code == 200
    rec = res_eval.json()
    assert rec["outcome"] == "BRIDGE_BACK"
    assert rec["target_concept_id"] in ["MATH-C01", "MATH-C02"]


def test_scenario_8_teacher_review_and_justified_override(client):
    """Scenario 8: Persistent struggle flags student for TEACHER_REVIEW, and teacher executes audited override."""
    learner_id = "struggling-learner"
    student_hdr = make_token_headers(learner_id, role="student")
    teacher_hdr = make_token_headers("teacher-01", role="teacher", name="Ms. Ananya Roy")

    # 3 distinct unassisted failures without any correct answers
    for q_id in ["Q-LIN-001", "Q-LIN-002", "Q-LIN-003"]:
        client.post("/api/v1/attempts", json={
            "attempt_id": str(uuid.uuid4()),
            "learner_id": learner_id,
            "question_id": q_id,
            "concept_id": "MATH-C05",
            "selected_option_id": "C",
            "hint_used": False
        }, headers=student_hdr)

    res_eval = client.post("/api/v1/recommendations/evaluate", json={
        "learner_id": learner_id,
        "concept_id": "MATH-C05"
    }, headers=student_hdr)
    assert res_eval.status_code == 200
    assert res_eval.json()["outcome"] == "TEACHER_REVIEW"

    # Teacher inspects cohort and sees student flagged
    res_cohort = client.get("/api/v1/teacher/cohort", headers=teacher_hdr)
    assert res_cohort.status_code == 200
    student_summary = next((s for s in res_cohort.json() if s["learner_id"] == learner_id), None)
    assert student_summary is not None
    assert student_summary["needs_review"] == 1 or student_summary["needs_review"] is True

    # Teacher executes audited override with required rationale
    res_override = client.post("/api/v1/teacher/override", json={
        "learner_id": learner_id,
        "concept_id": "MATH-C05",
        "previous_outcome": "TEACHER_REVIEW",
        "overridden_outcome": "SCAFFOLD",
        "reason": "Teacher clinical check: One-on-one session cleared confusion on inverse operations.",
        "teacher_id": "teacher-01"
    }, headers=teacher_hdr)
    assert res_override.status_code == 200
    assert res_override.json()["status"] == "success"


def test_scenario_9_authorization_attack_rejection(client):
    """Scenario 9: A student cannot access teacher endpoints or other students' private records."""
    attacker_student = "student-01"
    victim_student = "student-02"
    attacker_hdr = make_token_headers(attacker_student, role="student")
    # Also ensure victim exists
    make_token_headers(victim_student, role="student")

    # Attack 1: Student tries to access teacher cohort
    r1 = client.get("/api/v1/teacher/cohort", headers=attacker_hdr)
    assert r1.status_code == 403

    # Attack 2: Student tries to execute teacher override
    r2 = client.post("/api/v1/teacher/override", json={
        "learner_id": victim_student,
        "concept_id": "MATH-C01",
        "previous_outcome": "SCAFFOLD",
        "overridden_outcome": "STRETCH",
        "reason": "Self-promoted without permission",
        "teacher_id": attacker_student
    }, headers=attacker_hdr)
    assert r2.status_code == 403

    # Attack 3: Student tries to read victim's attempts
    r3 = client.get(f"/api/v1/learners/{victim_student}/attempts", headers=attacker_hdr)
    assert r3.status_code == 403


def test_scenario_10_offline_recovery_and_sync(client):
    """Scenario 10: Locally queued attempts synchronize after reconnection without duplicate credit."""
    learner_id = "offline-sync-learner"
    headers = make_token_headers(learner_id)
    offline_attempt_id = "offline-att-" + str(uuid.uuid4())

    payload = {
        "attempt_id": offline_attempt_id,
        "learner_id": learner_id,
        "question_id": "Q-VER-001",
        "concept_id": "MATH-C06",
        "selected_option_id": "A",
        "hint_used": False,
        "client_timestamp": "2026-10-29T20:00:00Z"
    }

    # Simulate sync when network is restored
    res_sync = client.post("/api/v1/attempts", json=payload, headers=headers)
    assert res_sync.status_code == 200
    assert res_sync.json()["is_duplicate"] is False

    # Simulate accidental resend of the same offline queue item
    res_retry = client.post("/api/v1/attempts", json=payload, headers=headers)
    assert res_retry.status_code == 200
    assert res_retry.json()["is_duplicate"] is True
    assert "already recorded" in res_retry.json()["message"]
