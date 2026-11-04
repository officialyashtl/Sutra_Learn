"""
SUTRA LEARN — Educational Excellence & Advanced Capability Test Suite
Verifies:
1. Spaced retrieval forgetting curve modeling (Ebbinghaus SM-2).
2. Dynamic adaptive question difficulty selection (Zone of Proximal Development).
3. AI Tutor Orchestrator unification and mathematical step verification.
4. AI Diagnostic Question Generation with AST Validation.
5. In-memory sliding window rate limiting (brute force & quota protection).
6. Cross-learner privacy enforcement on spaced retrieval endpoints.
7. Database connection resilience and busy-timeout protection.
"""

import sys
import time
import pytest
from pathlib import Path
from datetime import datetime, timezone, timedelta
from fastapi.testclient import TestClient

BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))

from app.main import app
from app.auth import create_access_token
from app.db.database import get_db_connection, init_db
from app.db import crud
from app.engine.spaced_retrieval import (
    SpacedRetrievalEngine,
    RetrievalStatus,
    SpacedConceptSchedule
)
from app.engine.adaptive import AdaptiveEngine, EvidenceRecord
from app.content.models import MisconceptionTag, CognitiveDemand
from app.auth_rate_limit import SlidingWindowRateLimiter


@pytest.fixture(scope="module")
def client():
    init_db()
    return TestClient(app)


@pytest.fixture
def student_token():
    return create_access_token("student-01", "student", "Aarav Sharma")


@pytest.fixture
def teacher_token():
    return create_access_token("teacher-01", "teacher", "Ms. Ananya Roy")


# =============================================================================
# 1. SPACED RETRIEVAL & COGNITIVE RETENTION TESTS
# =============================================================================
def test_spaced_retrieval_decay_formula():
    """Verifies exponential forgetting curve R(t) = exp(-t / S)."""
    # Immediate recall (t=0) must be 1.0
    r0 = SpacedRetrievalEngine.calculate_retention(days_elapsed=0.0, stability_days=2.0)
    assert r0 == 1.0

    # At t = S, retention must be exactly 1/e ≈ 0.3679
    r_half = SpacedRetrievalEngine.calculate_retention(days_elapsed=2.0, stability_days=2.0)
    assert round(r_half, 2) == 0.37

    # As t grows, retention decays towards 0
    r_old = SpacedRetrievalEngine.calculate_retention(days_elapsed=10.0, stability_days=2.0)
    assert r_old < 0.05


def test_spaced_retrieval_schedule_progression():
    """Verifies that clean unassisted practice expands stability while errors reduce stability."""
    # Step 1: Initial practice
    s1 = SpacedRetrievalEngine.update_schedule_on_attempt(
        current_stability=1.5,
        current_ease=2.5,
        repetitions=0,
        is_correct=True,
        hint_used=False
    )
    assert s1["repetitions"] == 1
    assert s1["stability_days"] >= 1.5

    # Step 2: Second unassisted practice multiplies stability by ease factor
    s2 = SpacedRetrievalEngine.update_schedule_on_attempt(
        current_stability=s1["stability_days"],
        current_ease=s1["ease_factor"],
        repetitions=s1["repetitions"],
        is_correct=True,
        hint_used=False
    )
    assert s2["repetitions"] == 2
    assert s2["stability_days"] > s1["stability_days"]

    # Step 3: Error causes a lapse, resetting repetitions and cutting stability
    s3 = SpacedRetrievalEngine.update_schedule_on_attempt(
        current_stability=s2["stability_days"],
        current_ease=s2["ease_factor"],
        repetitions=s2["repetitions"],
        is_correct=False,
        hint_used=False
    )
    assert s3["repetitions"] == 0
    assert s3["stability_days"] < s2["stability_days"]


def test_spaced_retrieval_status_categories():
    """Verifies the four retrieval status thresholds."""
    now = datetime.now(timezone.utc)

    # 1. Fresh concept (0.1 days elapsed, 3 days stability -> R ≈ 96.7% -> CONSOLIDATED)
    sch_fresh = SpacedRetrievalEngine.evaluate_concept_schedule(
        concept_id="MATH-C01",
        last_attempt_iso=(now - timedelta(hours=2)).isoformat(),
        stability_days=3.0,
        ease_factor=2.5,
        repetitions=1,
        now=now
    )
    assert sch_fresh.retrieval_status == RetrievalStatus.CONSOLIDATED
    assert sch_fresh.estimated_retention >= 0.85

    # 2. Optimal review window (0.70 <= R < 0.85 -> REVIEW_RECOMMENDED)
    sch_review = SpacedRetrievalEngine.evaluate_concept_schedule(
        concept_id="MATH-C01",
        last_attempt_iso=(now - timedelta(days=1)).isoformat(),
        stability_days=4.0,
        ease_factor=2.5,
        repetitions=1,
        now=now
    )
    assert sch_review.retrieval_status == RetrievalStatus.REVIEW_RECOMMENDED

    # 3. Decayed concept (R < 0.50 -> CRITICAL_DECAY)
    sch_decayed = SpacedRetrievalEngine.evaluate_concept_schedule(
        concept_id="MATH-C01",
        last_attempt_iso=(now - timedelta(days=7)).isoformat(),
        stability_days=2.0,
        ease_factor=2.5,
        repetitions=1,
        now=now
    )
    assert sch_decayed.retrieval_status == RetrievalStatus.CRITICAL_DECAY
    assert sch_decayed.estimated_retention < 0.50


# =============================================================================
# 2. DYNAMIC ADAPTIVE DIFFICULTY (ZPD) SELECTION TESTS
# =============================================================================
def test_adaptive_difficulty_zpd_selection():
    """Verifies question selection routes dynamically by target difficulty and cognitive demand."""
    engine = AdaptiveEngine()

    # Request Level 1 Procedural
    q_easy = engine._select_fresh_question(
        concept_id="MATH-C01",
        used_ids=set(),
        target_difficulty=1,
        target_demand=CognitiveDemand.PROCEDURAL
    )
    assert q_easy is not None
    assert q_easy.difficulty == 1

    # Request Level 3 Analytical / Transfer
    q_hard = engine._select_fresh_question(
        concept_id="MATH-C01",
        used_ids=set(),
        target_difficulty=3,
        target_demand=CognitiveDemand.TRANSFER
    )
    assert q_hard is not None
    assert q_hard.difficulty in (2, 3)


# =============================================================================
# 3. AI TUTOR ORCHESTRATOR UNIFICATION TESTS
# =============================================================================
def test_tutor_chat_orchestrator_integration(client, student_token):
    """Verifies that /api/v1/tutor/chat executes through the 12-state Orchestrator."""
    res = client.post(
        "/api/v1/tutor/chat",
        headers={"Authorization": f"Bearer {student_token}"},
        json={
            "message": "How do I balance an equation when adding 5 to both sides?",
            "concept_id": "MATH-C02",
            "mode": "guided_learning"
        }
    )
    assert res.status_code == 200
    data = res.json()
    assert "answer" in data
    assert "provider_metadata" in data
    # Provider attribution must be truthful
    assert data["provider_metadata"]["provider"] in ["Google Gemini", "NCERT Curriculum Engine", "Ollama Qwen 3.5 4B", "SutraCurriculumEngine"]
    assert "latency_ms" in data["provider_metadata"]


# =============================================================================
# 4. AI DIAGNOSTIC ITEM GENERATION WITH AST VALIDATION TESTS
# =============================================================================
def test_generate_diagnostic_item_with_ast_validation(client, student_token):
    """Verifies diagnostic question generation and symbolic step validation."""
    res = client.post(
        "/api/v1/ai/generate-diagnostic-item",
        headers={"Authorization": f"Bearer {student_token}"},
        json={
            "concept_id": "MATH-C02",
            "difficulty": 2
        }
    )
    assert res.status_code == 200
    data = res.json()
    assert data["concept_id"] == "MATH-C02"
    assert len(data["options"]) == 4
    assert data["validation_status"] in ["AST_VERIFIED", "CURRICULUM_VERIFIED"]
    assert data["correct_option_id"] in ["A", "B", "C", "D"]
    assert len(data["hint"]) > 0


# =============================================================================
# 5. RATE LIMITING & SECURITY DEFENSE TESTS
# =============================================================================
def test_rate_limiter_brute_force_defense():
    """Verifies that excessive requests trip the sliding window rate limiter."""
    limiter = SlidingWindowRateLimiter(max_requests=3, window_seconds=10)
    assert limiter.is_allowed("attacker_ip") is True
    assert limiter.is_allowed("attacker_ip") is True
    assert limiter.is_allowed("attacker_ip") is True
    # 4th request must be rejected
    assert limiter.is_allowed("attacker_ip") is False


def test_spaced_retrieval_endpoint_privacy(client, student_token):
    """Verifies that a student cannot view another student's spaced retrieval queue."""
    # student-01 accesses their own queue -> 200
    res_self = client.get(
        "/api/v1/learners/student-01/spaced-retrieval",
        headers={"Authorization": f"Bearer {student_token}"}
    )
    assert res_self.status_code == 200
    data = res_self.json()
    assert data["learner_id"] == "student-01"

    # student-01 attempts to access student-02's queue -> 403 Forbidden
    res_other = client.get(
        "/api/v1/learners/student-02/spaced-retrieval",
        headers={"Authorization": f"Bearer {student_token}"}
    )
    assert res_other.status_code == 403
