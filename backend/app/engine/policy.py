"""
SUTRA LEARN - Adaptive Engine Decision Policy
Explicit, versioned, configurable rules and pedagogical thresholds.
"""

from pydantic import BaseModel, Field


class AdaptivePolicyConfig(BaseModel):
    """
    Pedagogical policy configuration.
    All criteria are explicit, documented, and deterministic.
    """
    policy_version: str = "1.0.0"

    # Evidence thresholds:
    # A single answer is never treated as conclusive mastery or permanent failure.
    min_attempts_for_mastery: int = Field(default=2, description="Minimum distinct items answered correctly for mastery")
    min_attempts_for_prereq_bridge: int = Field(default=2, description="Minimum distinct errors implicating a prerequisite before bridge back")
    
    # Mastery and proficiency thresholds
    mastery_accuracy_threshold: float = Field(default=0.85, description="Unassisted accuracy required for STRETCH")
    scaffold_accuracy_threshold: float = Field(default=0.50, description="Accuracy boundary for SCAFFOLD guided practice")
    
    # Escalation thresholds
    max_consecutive_errors_before_review: int = Field(default=3, description="Triggers TEACHER_REVIEW if student struggles persistently")
    
    # Weight penalties for assistance
    hint_penalty_factor: float = Field(default=0.5, description="Assisted correct responses carry half the evidence weight of unassisted")


DEFAULT_POLICY = AdaptivePolicyConfig()

