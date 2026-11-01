"""
SUTRA LEARN - Pydantic Request & Response Schemas
Type-safe API contracts for assessment, attempts, evaluation, progress, and teacher controls.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from app.content.models import Option, CognitiveDemand, MisconceptionTag, WorkedStep, Lesson


class ConceptSummary(BaseModel):
    id: str
    code: str
    title: str
    grade: int
    subject: str
    description: str
    prerequisites: List[str]
    order_index: int
    is_unlocked: bool = True
    missing_prerequisites: List[str] = Field(default_factory=list)


class ConceptDetail(ConceptSummary):
    lesson: Lesson


class AssessmentQuestionOut(BaseModel):
    id: str
    concept_id: str
    prompt: str
    equation_display: Optional[str] = None
    options: List[Option]
    hint: str
    difficulty: int
    cognitive_demand: CognitiveDemand


class AttemptCreate(BaseModel):
    attempt_id: str = Field(..., description="Unique client-generated UUID for idempotency")
    learner_id: str
    question_id: str
    concept_id: str
    selected_option_id: str
    hint_used: bool = False
    session_id: Optional[str] = None
    client_timestamp: Optional[str] = None


class AttemptResult(BaseModel):
    attempt_id: str
    is_duplicate: bool
    is_correct: bool
    hint_used: bool
    selected_option_id: str
    correct_option_id: str
    explanation: str
    misconception_tag: str
    misconception_explanation: Optional[str] = None
    message: str


class EvaluationRequest(BaseModel):
    learner_id: str
    concept_id: str


class RecommendationResponse(BaseModel):
    id: str
    learner_id: str
    concept_id: str
    outcome: str
    target_concept_id: str
    target_concept_title: str
    target_activity_type: str
    target_activity_id: Optional[str] = None
    reason_code: str
    explanation: str
    confidence_score: float
    evidence_summary: Dict[str, Any]
    policy_version: str


class TeacherOverrideRequest(BaseModel):
    learner_id: str
    concept_id: str
    previous_outcome: str
    overridden_outcome: str
    reason: str
    teacher_id: str

