"""
SUTRA LEARN — Spaced Retrieval & Long-Term Memory Engine
Grounded in Ebbinghaus Forgetting Curve and SuperMemo SM-2 interval principles.
Calculates cognitive retention, review schedules, and spaced retrieval queues
to ensure sustainable long-term mathematical mastery.
"""

import math
import time
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone, timedelta
from pydantic import BaseModel, Field

from app.content.concepts import CONCEPTS_REGISTRY


class RetrievalStatus:
    CONSOLIDATED = "CONSOLIDATED"             # R >= 0.85: Strong memory trace
    REVIEW_RECOMMENDED = "REVIEW_RECOMMENDED" # 0.70 <= R < 0.85: Optimal retrieval window
    DUE_NOW = "DUE_NOW"                       # 0.50 <= R < 0.70: Retention decaying
    CRITICAL_DECAY = "CRITICAL_DECAY"         # R < 0.50: Significant lapse risk


class SpacedConceptSchedule(BaseModel):
    concept_id: str
    concept_title: str
    last_practiced_at: str
    days_elapsed: float
    stability_days: float
    ease_factor: float
    repetition_count: int
    estimated_retention: float = Field(ge=0.0, le=1.0)
    retrieval_status: str
    urgency_score: float  # Higher means more urgent
    next_review_due: str
    recommended_action: str
    cognitive_rationale: str


class SpacedRetrievalQueue(BaseModel):
    learner_id: str
    total_evaluated_concepts: int
    due_count: int
    review_queue: List[SpacedConceptSchedule]
    retention_average: float
    generated_at: str


class SpacedRetrievalEngine:
    DEFAULT_EASE_FACTOR = 2.5
    MIN_EASE_FACTOR = 1.3
    BASE_STABILITY_DAYS = 1.5

    @classmethod
    def calculate_retention(cls, days_elapsed: float, stability_days: float) -> float:
        """
        Calculates memory retention probability using the classic exponential forgetting curve:
        R(t) = exp(-t / S)
        where t is days elapsed and S is memory stability in days.
        """
        if stability_days <= 0:
            stability_days = cls.BASE_STABILITY_DAYS
        if days_elapsed <= 0:
            return 1.0
        exponent = -days_elapsed / stability_days
        retention = math.exp(exponent)
        return max(0.0, min(1.0, round(retention, 4)))

    @classmethod
    def update_schedule_on_attempt(
        cls,
        current_stability: float,
        current_ease: float,
        repetitions: int,
        is_correct: bool,
        hint_used: bool,
        days_since_last: float = 0.0
    ) -> Dict[str, Any]:
        """
        Computes updated stability, ease factor, and interval following an assessment attempt.
        """
        stability = current_stability if current_stability > 0 else cls.BASE_STABILITY_DAYS
        ease = current_ease if current_ease >= cls.MIN_EASE_FACTOR else cls.DEFAULT_EASE_FACTOR

        if is_correct:
            if not hint_used:
                # Clean unassisted success strengthens memory significantly
                reps = repetitions + 1
                if reps == 1:
                    new_stability = cls.BASE_STABILITY_DAYS
                elif reps == 2:
                    new_stability = cls.BASE_STABILITY_DAYS * ease
                else:
                    new_stability = max(stability * ease, stability + 2.0)
                # Slightly increase ease factor for confident retrieval
                new_ease = min(3.0, ease + 0.1)
            else:
                # Assisted success provides partial memory consolidation
                reps = repetitions
                new_stability = max(stability * 1.2, stability + 0.5)
                new_ease = max(cls.MIN_EASE_FACTOR, ease - 0.05)
        else:
            # Lapse / error: memory trace compromised, stability resets with penalization
            reps = 0
            new_stability = max(1.0, stability * 0.5)
            new_ease = max(cls.MIN_EASE_FACTOR, ease - 0.2)

        new_stability = round(new_stability, 2)
        new_ease = round(new_ease, 2)
        return {
            "stability_days": new_stability,
            "ease_factor": new_ease,
            "repetitions": reps
        }

    @classmethod
    def evaluate_concept_schedule(
        cls,
        concept_id: str,
        last_attempt_iso: str,
        stability_days: float,
        ease_factor: float,
        repetitions: int,
        now: Optional[datetime] = None
    ) -> SpacedConceptSchedule:
        """
        Evaluates the current spaced retrieval schedule and retention for a concept.
        """
        concept = CONCEPTS_REGISTRY.get(concept_id)
        concept_title = concept.title if concept else concept_id

        now_dt = now or datetime.now(timezone.utc)
        try:
            # Support both ISO strings with or without timezone
            clean_ts = last_attempt_iso.replace("Z", "+00:00")
            if "+" in clean_ts or "-" in clean_ts[10:]:
                last_dt = datetime.fromisoformat(clean_ts)
            else:
                last_dt = datetime.fromisoformat(clean_ts).replace(tzinfo=timezone.utc)
        except Exception:
            last_dt = now_dt - timedelta(days=1.0)

        elapsed_seconds = max(0.0, (now_dt - last_dt).total_seconds())
        days_elapsed = round(elapsed_seconds / 86400.0, 2)

        retention = cls.calculate_retention(days_elapsed, stability_days)

        # Categorize status
        if retention >= 0.85:
            status = RetrievalStatus.CONSOLIDATED
            urgency = round(1.0 - retention, 3)
            rec_action = "Maintain mastery trajectory; concept memory is currently consolidated."
            rationale = (
                f"Memory trace for '{concept_title}' is robust ({int(retention*100)}% estimated retention). "
                f"Consolidation stability is {stability_days} days."
            )
        elif retention >= 0.70:
            status = RetrievalStatus.REVIEW_RECOMMENDED
            urgency = round(1.5 - retention, 3)
            rec_action = f"Schedule a brief 2-question retention check within the next {max(1, int(stability_days * 0.3))} days."
            rationale = (
                f"Concept has reached the optimal retrieval window (70-85% retention). "
                f"Active recall now produces maximal long-term cognitive potentiation."
            )
        elif retention >= 0.50:
            status = RetrievalStatus.DUE_NOW
            urgency = round(2.0 - retention, 3)
            rec_action = f"Complete active retrieval practice on '{concept_title}' before advancing to dependent concepts."
            rationale = (
                f"Retention has decayed to {int(retention*100)}% after {days_elapsed} days. "
                f"A quick retrieval check prevents complete forgetting."
            )
        else:
            status = RetrievalStatus.CRITICAL_DECAY
            urgency = round(3.0 - retention, 3)
            rec_action = f"Priority reinforcement required. Revisit worked steps and complete foundational practice."
            rationale = (
                f"Significant memory decay detected ({int(retention*100)}% retention). "
                f"Immediate review prevents compounding difficulty on downstream curriculum modules."
            )

        due_date = last_dt + timedelta(days=stability_days)
        due_iso = due_date.isoformat()

        return SpacedConceptSchedule(
            concept_id=concept_id,
            concept_title=concept_title,
            last_practiced_at=last_dt.isoformat(),
            days_elapsed=days_elapsed,
            stability_days=stability_days,
            ease_factor=ease_factor,
            repetition_count=repetitions,
            estimated_retention=retention,
            retrieval_status=status,
            urgency_score=urgency,
            next_review_due=due_iso,
            recommended_action=rec_action,
            cognitive_rationale=rationale
        )

