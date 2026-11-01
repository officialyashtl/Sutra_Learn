"""
SUTRA LEARN - Content Domain Models
Strongly typed models for concepts, prerequisite graphs, questions, and learning lessons.
"""

from enum import Enum
from typing import List, Optional, Dict
from pydantic import BaseModel, Field


class CognitiveDemand(str, Enum):
    RECALL = "recall"
    PROCEDURAL = "procedural"
    CONCEPTUAL = "conceptual"
    TRANSFER = "transfer"


class MisconceptionTag(str, Enum):
    NONE = "none"
    SIGN_ERROR = "sign_error"                      # e.g., adding instead of subtracting a negative
    INVERSE_OPERATION_CONFUSION = "inverse_conf"    # e.g., dividing instead of multiplying
    UNBALANCED_OPERATION = "unbalanced_operation"  # applied to one side only
    LIKE_TERMS_CONFLATION = "like_terms_conflation" # adding variable to constant (e.g. 2x + 3 = 5x)
    DISTRIBUTION_INCOMPLETE = "distrib_incomplete"  # forgetting to multiply inner terms
    SUBSTITUTION_CALC_ERROR = "sub_calc_error"     # arithmetic error during check
    RECIPROCAL_CONFUSION = "reciprocal_confusion"   # dividing fractions without inverting
    EXPONENT_BASE_CONFLATION = "exponent_base_conflation" # e.g. 2^3 = 6 or a^m * a^n = a^(mn)
    SQUARE_ROOT_HALVING = "square_root_halving"     # e.g. sqrt(16) = 8
    PERCENTAGE_BASE_ERROR = "percentage_base_error" # wrong base for percentage calculation
    AREA_PERIMETER_CONFUSION = "area_perimeter_confusion" # confusing area with perimeter formulas
    PROPORTION_INVERSION = "proportion_inversion"   # treating inverse proportion as direct
    QUADRILATERAL_ANGLE_SUM_ERROR = "quad_angle_sum_error" # angle sum error in polygons


class Option(BaseModel):
    id: str = Field(..., description="Option key, e.g. 'A', 'B', 'C', 'D'")
    text: str = Field(..., description="Text or mathematical expression of choice")
    is_correct: bool = False
    misconception_tag: MisconceptionTag = MisconceptionTag.NONE
    misconception_explanation: Optional[str] = None


class WorkedStep(BaseModel):
    step_number: int
    action: str
    expression: str
    reasoning: str


class Lesson(BaseModel):
    concept_id: str
    title: str
    objective: str
    key_principles: List[str]
    worked_steps: List[WorkedStep]
    common_pitfalls: List[str]
    interactive_prompt: str


class Question(BaseModel):
    id: str
    concept_id: str
    prerequisite_ids: List[str] = Field(default_factory=list)
    prompt: str
    equation_display: Optional[str] = None
    options: List[Option]
    correct_option_id: str
    hint: str
    explanation: str
    cognitive_demand: CognitiveDemand
    difficulty: int = Field(ge=1, le=5)
    content_version: str = "1.0.0"


class Concept(BaseModel):
    id: str
    code: str
    title: str
    grade: int = 8
    subject: str = "Mathematics"
    description: str
    prerequisites: List[str] = Field(default_factory=list)
    order_index: int
    lesson: Lesson

