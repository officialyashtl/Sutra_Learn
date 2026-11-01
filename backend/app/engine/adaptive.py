"""
SUTRA LEARN - Deterministic Adaptive Engine
Pure, decoupled educational reasoning engine.
Translates student assessment evidence into pedagogical next steps:
BRIDGE_BACK, SCAFFOLD, STRETCH, CONFIRM, or TEACHER_REVIEW.
"""

from enum import Enum
from typing import List, Dict, Optional, Set
from pydantic import BaseModel, Field

from ..content.models import MisconceptionTag, CognitiveDemand
from ..content.concepts import CONCEPTS_REGISTRY, get_prerequisite_graph
from ..content.questions import QUESTIONS_REGISTRY, get_questions_by_concept
from .policy import AdaptivePolicyConfig, DEFAULT_POLICY


class LearningPathOutcome(str, Enum):
    BRIDGE_BACK = "BRIDGE_BACK"
    SCAFFOLD = "SCAFFOLD"
    STRETCH = "STRETCH"
    CONFIRM = "CONFIRM"
    TEACHER_REVIEW = "TEACHER_REVIEW"


class EvidenceRecord(BaseModel):
    attempt_id: str
    question_id: str
    concept_id: str
    is_correct: bool
    hint_used: bool = False
    selected_option_id: str
    misconception_tag: MisconceptionTag = MisconceptionTag.NONE
    cognitive_demand: CognitiveDemand = CognitiveDemand.PROCEDURAL
    timestamp: Optional[str] = None


class Recommendation(BaseModel):
    outcome: LearningPathOutcome
    target_concept_id: str
    target_concept_title: str
    target_activity_type: str  # "lesson" | "practice" | "diagnostic" | "challenge" | "teacher_intervention"
    target_activity_id: Optional[str] = None
    reason_code: str
    explanation: str
    confidence_score: float = Field(ge=0.0, le=1.0)
    evidence_summary: Dict[str, object]
    policy_version: str
    content_version: str = "1.0.0"


# Mapping from root misconception to the exact prerequisite concept that teaches it
MISCONCEPTION_TO_PREREQUISITE_MAP: Dict[str, str] = {
    MisconceptionTag.SIGN_ERROR.value: "MATH-C01",                  # Integer Arithmetic
    MisconceptionTag.UNBALANCED_OPERATION.value: "MATH-C02",        # Equality & Balance
    MisconceptionTag.INVERSE_OPERATION_CONFUSION.value: "MATH-C03", # Inverse Operations
    MisconceptionTag.LIKE_TERMS_CONFLATION.value: "MATH-C04",       # Simplifying Expressions
    MisconceptionTag.DISTRIBUTION_INCOMPLETE.value: "MATH-C04",     # Simplifying Expressions
    MisconceptionTag.SUBSTITUTION_CALC_ERROR.value: "MATH-C01",     # Integer Arithmetic
    MisconceptionTag.RECIPROCAL_CONFUSION.value: "MATH-C07",        # Rational Numbers
    MisconceptionTag.EXPONENT_BASE_CONFLATION.value: "MATH-C23",    # Exponents & Powers
    MisconceptionTag.SQUARE_ROOT_HALVING.value: "MATH-C13",         # Squares and Square Roots
    MisconceptionTag.PERCENTAGE_BASE_ERROR.value: "MATH-C17",       # Comparing Quantities
    MisconceptionTag.AREA_PERIMETER_CONFUSION.value: "MATH-C21",    # Mensuration
    MisconceptionTag.PROPORTION_INVERSION.value: "MATH-C25",        # Direct & Inverse Proportions
    MisconceptionTag.QUADRILATERAL_ANGLE_SUM_ERROR.value: "MATH-C09", # Quadrilaterals
}


class AdaptiveEngine:
    def __init__(self, policy: AdaptivePolicyConfig = DEFAULT_POLICY):
        self.policy = policy
        self.prereq_graph = get_prerequisite_graph()

    def evaluate_learner_concept(
        self,
        current_concept_id: str,
        evidence: List[EvidenceRecord],
        unlocked_concepts: Optional[List[str]] = None
    ) -> Recommendation:
        """
        Pure deterministic decision pipeline.
        Evaluates a sequence of attempt records for a specific concept.
        """
        concept = CONCEPTS_REGISTRY.get(current_concept_id)
        if not concept:
            return Recommendation(
                outcome=LearningPathOutcome.TEACHER_REVIEW,
                target_concept_id=current_concept_id,
                target_concept_title="Unknown Concept",
                target_activity_type="teacher_intervention",
                target_activity_id=None,
                reason_code="REV_UNKNOWN_CONCEPT",
                explanation=f"Concept ID '{current_concept_id}' is not in the curriculum registry.",
                confidence_score=1.0,
                evidence_summary={"error": "concept_missing"},
                policy_version=self.policy.policy_version
            )

        # Filter evidence for this concept
        concept_evidence = [e for e in evidence if e.concept_id == current_concept_id]

        # Repeated attempts at the same memorized question must NOT be treated as independent evidence.
        distinct_attempts: Dict[str, EvidenceRecord] = {}
        for ev in concept_evidence:
            distinct_attempts[ev.question_id] = ev  # latest attempt for this question

        distinct_list = list(distinct_attempts.values())
        total_distinct = len(distinct_list)

        # 1. Check for Insufficient Evidence -> CONFIRM
        if total_distinct < self.policy.min_attempts_for_mastery:
            fresh_question = self._select_fresh_question(current_concept_id, set(distinct_attempts.keys()))
            return Recommendation(
                outcome=LearningPathOutcome.CONFIRM,
                target_concept_id=current_concept_id,
                target_concept_title=concept.title,
                target_activity_type="diagnostic",
                target_activity_id=fresh_question.id if fresh_question else None,
                reason_code="CONF_INSUFFICIENT_EVIDENCE",
                explanation=(
                    f"Only {total_distinct} unique question(s) assessed so far. "
                    f"SUTRA LEARN requires at least {self.policy.min_attempts_for_mastery} distinct diagnostic items "
                    f"before drawing a conclusive recommendation, ensuring every learner receives fair, evidence-based guidance."
                ),
                confidence_score=0.40,
                evidence_summary={
                    "distinct_questions_evaluated": total_distinct,
                    "min_required": self.policy.min_attempts_for_mastery
                },
                policy_version=self.policy.policy_version
            )

        # Analyze evidence metrics across distinct questions
        unassisted_correct = 0
        assisted_correct = 0
        incorrect_count = 0
        misconception_counts: Dict[str, int] = {}
        prereq_signals: Dict[str, int] = {p: 0 for p in concept.prerequisites}

        for ev in distinct_list:
            if ev.is_correct:
                if ev.hint_used:
                    assisted_correct += 1
                else:
                    unassisted_correct += 1
            else:
                incorrect_count += 1
                if ev.misconception_tag != MisconceptionTag.NONE:
                    tag_str = str(ev.misconception_tag.value)
                    misconception_counts[tag_str] = misconception_counts.get(tag_str, 0) + 1

                # Check if question links to specific prerequisites
                q = QUESTIONS_REGISTRY.get(ev.question_id)
                if q:
                    for pr in q.prerequisite_ids:
                        if pr in prereq_signals:
                            prereq_signals[pr] += 1

        weighted_score = (
            (unassisted_correct * 1.0) +
            (assisted_correct * self.policy.hint_penalty_factor)
        ) / total_distinct

        unassisted_accuracy = unassisted_correct / total_distinct

        summary_data = {
            "total_distinct": total_distinct,
            "unassisted_correct": unassisted_correct,
            "assisted_correct": assisted_correct,
            "incorrect_count": incorrect_count,
            "unassisted_accuracy": round(unassisted_accuracy, 2),
            "weighted_score": round(weighted_score, 2),
            "misconception_counts": misconception_counts,
            "prerequisite_gap_signals": prereq_signals
        }

        # 2. Check for Persistent Failure -> TEACHER_REVIEW
        if incorrect_count >= self.policy.max_consecutive_errors_before_review and unassisted_correct == 0:
            return Recommendation(
                outcome=LearningPathOutcome.TEACHER_REVIEW,
                target_concept_id=current_concept_id,
                target_concept_title=concept.title,
                target_activity_type="teacher_intervention",
                target_activity_id=None,
                reason_code="REV_PERSISTENT_STRUGGLE",
                explanation=(
                    f"Student has encountered difficulty across {incorrect_count} distinct items on '{concept.title}' "
                    f"without reaching a confirmed resolution. To prevent student frustration, automated progression is paused "
                    f"and flagged for human teacher insight and targeted one-on-one intervention."
                ),
                confidence_score=0.90,
                evidence_summary=summary_data,
                policy_version=self.policy.policy_version
            )

        # 3. Check for Specific Misconception Patterns -> BRIDGE_BACK (Highest diagnostic specificity)
        for tag_str, count in misconception_counts.items():
            if count >= self.policy.min_attempts_for_prereq_bridge:
                target_prereq = MISCONCEPTION_TO_PREREQUISITE_MAP.get(tag_str)
                if target_prereq and target_prereq in CONCEPTS_REGISTRY and target_prereq != current_concept_id:
                    prereq_c = CONCEPTS_REGISTRY[target_prereq]
                    return Recommendation(
                        outcome=LearningPathOutcome.BRIDGE_BACK,
                        target_concept_id=target_prereq,
                        target_concept_title=prereq_c.title,
                        target_activity_type="lesson",
                        target_activity_id=f"lesson-{target_prereq.lower()}",
                        reason_code=f"BRIDGE_MISCONCEPTION_{tag_str.upper()}",
                        explanation=(
                            f"Diagnostic evidence reveals repeated error patterns tagged as '{tag_str}' ({count} times). "
                            f"A targeted review of prerequisite '{prereq_c.title}' is recommended to address the underlying root cause."
                        ),
                        confidence_score=0.92,
                        evidence_summary=summary_data,
                        policy_version=self.policy.policy_version
                    )

        # 4. Check for General Prerequisite Gap from Question Links -> BRIDGE_BACK
        for prereq_id, signal_count in prereq_signals.items():
            if signal_count >= self.policy.min_attempts_for_prereq_bridge:
                prereq_concept = CONCEPTS_REGISTRY.get(prereq_id)
                prereq_title = prereq_concept.title if prereq_concept else prereq_id
                return Recommendation(
                    outcome=LearningPathOutcome.BRIDGE_BACK,
                    target_concept_id=prereq_id,
                    target_concept_title=prereq_title,
                    target_activity_type="lesson",
                    target_activity_id=f"lesson-{prereq_id.lower()}",
                    reason_code="BRIDGE_PREREQUISITE_GAP",
                    explanation=(
                        f"Analysis indicates an underlying foundation gap in prerequisite '{prereq_title}' "
                        f"based on {signal_count} observed errors. Before advancing in '{concept.title}', "
                        f"reinforcing this prerequisite ensures sustainable mastery."
                    ),
                    confidence_score=0.88,
                    evidence_summary=summary_data,
                    policy_version=self.policy.policy_version
                )

        # 5. Check for Mastery -> STRETCH
        if unassisted_accuracy >= self.policy.mastery_accuracy_threshold and total_distinct >= self.policy.min_attempts_for_mastery:
            next_concept = self._get_next_concept(current_concept_id)
            if next_concept:
                target_id = next_concept.id
                target_title = next_concept.title
                act_type = "lesson"
            else:
                target_id = current_concept_id
                target_title = f"{concept.title} (Advanced Challenge)"
                act_type = "challenge"

            return Recommendation(
                outcome=LearningPathOutcome.STRETCH,
                target_concept_id=target_id,
                target_concept_title=target_title,
                target_activity_type=act_type,
                target_activity_id=f"act-stretch-{target_id.lower()}",
                reason_code="STRETCH_MASTERY_DEMONSTRATED",
                explanation=(
                    f"Demonstrated mastery on '{concept.title}' with {unassisted_correct}/{total_distinct} "
                    f"unassisted correct answers ({int(unassisted_accuracy * 100)}% accuracy). "
                    f"Ready for advanced stretch challenges and progression."
                ),
                confidence_score=0.95,
                evidence_summary=summary_data,
                policy_version=self.policy.policy_version
            )

        # 6. Check for Developing Understanding -> SCAFFOLD
        if (weighted_score >= self.policy.scaffold_accuracy_threshold or assisted_correct > 0 or unassisted_correct > 0):
            return Recommendation(
                outcome=LearningPathOutcome.SCAFFOLD,
                target_concept_id=current_concept_id,
                target_concept_title=concept.title,
                target_activity_type="practice",
                target_activity_id=f"practice-guided-{current_concept_id.lower()}",
                reason_code="SCAFF_DEVELOPING_UNDERSTANDING",
                explanation=(
                    f"Understanding of '{concept.title}' is actively developing "
                    f"(Score: {int(weighted_score * 100)}%, {assisted_correct} item(s) solved with hints). "
                    f"Structured scaffolding with guided practice and worked examples will solidify retention."
                ),
                confidence_score=0.82,
                evidence_summary=summary_data,
                policy_version=self.policy.policy_version
            )

        # 7. Fallback / Conflicting -> CONFIRM
        fresh_q = self._select_fresh_question(current_concept_id, set(distinct_attempts.keys()))
        return Recommendation(
            outcome=LearningPathOutcome.CONFIRM,
            target_concept_id=current_concept_id,
            target_concept_title=concept.title,
            target_activity_type="diagnostic",
            target_activity_id=fresh_q.id if fresh_q else None,
            reason_code="CONF_CONFLICTING_SIGNALS",
            explanation="Evidence demonstrates mixed signals. Gathering a clarifying assessment to confirm readiness.",
            confidence_score=0.60,
            evidence_summary=summary_data,
            policy_version=self.policy.policy_version
        )

    def _select_fresh_question(self, concept_id: str, used_ids: Set[str]):
        available = [q for q in get_questions_by_concept(concept_id) if q.id not in used_ids]
        if available:
            return available[0]
        all_q = get_questions_by_concept(concept_id)
        return all_q[0] if all_q else None

    def _get_next_concept(self, current_concept_id: str):
        concepts = sorted(list(CONCEPTS_REGISTRY.values()), key=lambda c: c.order_index)
        for i, c in enumerate(concepts):
            if c.id == current_concept_id and i + 1 < len(concepts):
                return concepts[i + 1]
        return None
