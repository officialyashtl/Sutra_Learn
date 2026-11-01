"""
Unit tests for the Deterministic Adaptive Engine.
Tests all 5 pedagogical outcomes:
CONFIRM, STRETCH, SCAFFOLD, BRIDGE_BACK, TEACHER_REVIEW,
as well as edge cases: duplicate questions, hint assistance weighting, and reproducibility.
"""

import pytest
from app.engine.adaptive import (
    AdaptiveEngine,
    EvidenceRecord,
    LearningPathOutcome
)
from app.content.models import MisconceptionTag, CognitiveDemand
from app.engine.policy import AdaptivePolicyConfig


@pytest.fixture
def engine():
    return AdaptiveEngine()


def test_insufficient_evidence_triggers_confirm(engine):
    """A single answer must NOT permanently classify a learner; it must trigger CONFIRM."""
    evidence = [
        EvidenceRecord(
            attempt_id="att-1",
            question_id="Q-INT-001",
            concept_id="MATH-C01",
            is_correct=False,
            hint_used=False,
            selected_option_id="B",
            misconception_tag=MisconceptionTag.SIGN_ERROR
        )
    ]
    rec = engine.evaluate_learner_concept("MATH-C01", evidence)
    assert rec.outcome == LearningPathOutcome.CONFIRM
    assert rec.reason_code == "CONF_INSUFFICIENT_EVIDENCE"
    assert rec.target_activity_type == "diagnostic"
    assert "at least 2 distinct" in rec.explanation


def test_duplicate_question_attempts_do_not_count_as_independent_evidence(engine):
    """Repeated attempts at the SAME question ID must not be treated as independent evidence."""
    evidence = [
        EvidenceRecord(
            attempt_id="att-1",
            question_id="Q-INT-001",
            concept_id="MATH-C01",
            is_correct=True,
            hint_used=False,
            selected_option_id="A"
        ),
        EvidenceRecord(
            attempt_id="att-2",
            question_id="Q-INT-001",  # Same question repeated
            concept_id="MATH-C01",
            is_correct=True,
            hint_used=False,
            selected_option_id="A"
        )
    ]
    # Despite 2 attempts in array, distinct count is 1 -> Must still CONFIRM
    rec = engine.evaluate_learner_concept("MATH-C01", evidence)
    assert rec.outcome == LearningPathOutcome.CONFIRM
    assert rec.reason_code == "CONF_INSUFFICIENT_EVIDENCE"


def test_mastery_triggers_stretch(engine):
    """Demonstrating unassisted correct answers across distinct questions triggers STRETCH."""
    evidence = [
        EvidenceRecord(
            attempt_id="att-1",
            question_id="Q-INT-001",
            concept_id="MATH-C01",
            is_correct=True,
            hint_used=False,
            selected_option_id="A"
        ),
        EvidenceRecord(
            attempt_id="att-2",
            question_id="Q-INT-002",
            concept_id="MATH-C01",
            is_correct=True,
            hint_used=False,
            selected_option_id="C"
        )
    ]
    rec = engine.evaluate_learner_concept("MATH-C01", evidence)
    assert rec.outcome == LearningPathOutcome.STRETCH
    assert rec.reason_code == "STRETCH_MASTERY_DEMONSTRATED"
    assert rec.confidence_score >= 0.90
    assert "unassisted correct" in rec.explanation


def test_hint_assistance_downgrades_to_scaffold(engine):
    """A correct answer after a hint is interpreted in context and triggers SCAFFOLD, not STRETCH."""
    evidence = [
        EvidenceRecord(
            attempt_id="att-1",
            question_id="Q-INT-001",
            concept_id="MATH-C01",
            is_correct=True,
            hint_used=True,  # Student needed a hint!
            selected_option_id="A"
        ),
        EvidenceRecord(
            attempt_id="att-2",
            question_id="Q-INT-002",
            concept_id="MATH-C01",
            is_correct=True,
            hint_used=False,
            selected_option_id="C"
        )
    ]
    rec = engine.evaluate_learner_concept("MATH-C01", evidence)
    assert rec.outcome == LearningPathOutcome.SCAFFOLD
    assert rec.reason_code == "SCAFF_DEVELOPING_UNDERSTANDING"
    assert "hints" in rec.explanation.lower()


def test_prerequisite_gap_triggers_bridge_back(engine):
    """Failing items in linear equations due to sign errors bridges back to Integer Arithmetic."""
    evidence = [
        EvidenceRecord(
            attempt_id="att-1",
            question_id="Q-LIN-001",
            concept_id="MATH-C05",
            is_correct=False,
            hint_used=False,
            selected_option_id="B",
            misconception_tag=MisconceptionTag.SIGN_ERROR
        ),
        EvidenceRecord(
            attempt_id="att-2",
            question_id="Q-LIN-002",
            concept_id="MATH-C05",
            is_correct=False,
            hint_used=False,
            selected_option_id="B",
            misconception_tag=MisconceptionTag.SIGN_ERROR
        )
    ]
    rec = engine.evaluate_learner_concept("MATH-C05", evidence)
    assert rec.outcome == LearningPathOutcome.BRIDGE_BACK
    assert rec.target_concept_id == "MATH-C01"  # Prerequisite Integer Arithmetic
    assert "MATH-C01" in rec.target_activity_id.upper() or "lesson" in rec.target_activity_id
    assert "BRIDGE" in rec.reason_code


def test_persistent_struggle_triggers_teacher_review(engine):
    """3 consecutive distinct unassisted errors with no correct answers triggers TEACHER_REVIEW."""
    evidence = [
        EvidenceRecord(
            attempt_id="att-1",
            question_id="Q-LIN-001",
            concept_id="MATH-C05",
            is_correct=False,
            hint_used=False,
            selected_option_id="C",
            misconception_tag=MisconceptionTag.UNBALANCED_OPERATION
        ),
        EvidenceRecord(
            attempt_id="att-2",
            question_id="Q-LIN-002",
            concept_id="MATH-C05",
            is_correct=False,
            hint_used=False,
            selected_option_id="C",
            misconception_tag=MisconceptionTag.DISTRIBUTION_INCOMPLETE
        ),
        EvidenceRecord(
            attempt_id="att-3",
            question_id="Q-LIN-003",
            concept_id="MATH-C05",
            is_correct=False,
            hint_used=False,
            selected_option_id="C",
            misconception_tag=MisconceptionTag.INVERSE_OPERATION_CONFUSION
        )
    ]
    rec = engine.evaluate_learner_concept("MATH-C05", evidence)
    assert rec.outcome == LearningPathOutcome.TEACHER_REVIEW
    assert rec.reason_code == "REV_PERSISTENT_STRUGGLE"
    assert rec.target_activity_type == "teacher_intervention"
    assert "human teacher insight" in rec.explanation


def test_deterministic_reproducibility(engine):
    """Identical evidence and policy must generate the identical recommendation every time."""
    evidence = [
        EvidenceRecord(
            attempt_id="att-1",
            question_id="Q-BAL-001",
            concept_id="MATH-C02",
            is_correct=True,
            hint_used=False,
            selected_option_id="B"
        ),
        EvidenceRecord(
            attempt_id="att-2",
            question_id="Q-BAL-002",
            concept_id="MATH-C02",
            is_correct=True,
            hint_used=False,
            selected_option_id="A"
        )
    ]
    rec1 = engine.evaluate_learner_concept("MATH-C02", evidence)
    rec2 = engine.evaluate_learner_concept("MATH-C02", evidence)
    assert rec1.model_dump() == rec2.model_dump()

