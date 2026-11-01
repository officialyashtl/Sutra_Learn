"""
SUTRA LEARN — AI Domain Models, Schemas and Enums
Defines strict types for Provider Registry, Health, Request Lifecycle,
Mathematical Validation, and Observability.
"""

from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class ProviderType(str, Enum):
    GEMINI = "gemini"
    OLLAMA_QWEN = "ollama_qwen"
    OLLAMA_GEMMA = "ollama_gemma"
    DETERMINISTIC = "deterministic"


class ProviderState(str, Enum):
    NOT_CONFIGURED = "NOT_CONFIGURED"
    DISABLED = "DISABLED"
    UNKNOWN = "UNKNOWN"
    CHECKING = "CHECKING"
    AVAILABLE = "AVAILABLE"
    DEGRADED = "DEGRADED"
    UNAVAILABLE = "UNAVAILABLE"
    CIRCUIT_OPEN = "CIRCUIT_OPEN"


class OrchestratorState(str, Enum):
    RECEIVED = "RECEIVED"
    VALIDATING = "VALIDATING"
    AUTHORIZING = "AUTHORIZING"
    BUILDING_CONTEXT = "BUILDING_CONTEXT"
    SELECTING_PROVIDER = "SELECTING_PROVIDER"
    GENERATING = "GENERATING"
    VALIDATING_OUTPUT = "VALIDATING_OUTPUT"
    PERSISTING = "PERSISTING"
    COMPLETED = "COMPLETED"
    FALLBACK = "FALLBACK"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class ErrorCategory(str, Enum):
    PERMANENT_AUTH = "PERMANENT_AUTH"
    PERMISSION_DENIED = "PERMISSION_DENIED"
    MODEL_NOT_FOUND = "MODEL_NOT_FOUND"
    QUOTA_EXCEEDED = "QUOTA_EXCEEDED"
    RATE_LIMITED = "RATE_LIMITED"
    NETWORK_FAILURE = "NETWORK_FAILURE"
    TIMEOUT = "TIMEOUT"
    SAFETY_REJECTION = "SAFETY_REJECTION"
    EMPTY_RESPONSE = "EMPTY_RESPONSE"
    MALFORMED_RESPONSE = "MALFORMED_RESPONSE"
    SDK_ERROR = "SDK_ERROR"
    UNKNOWN = "UNKNOWN"


class ProviderHealth(BaseModel):
    provider_id: str
    display_name: str
    provider_type: ProviderType
    configured: bool
    enabled: bool
    model_id: str
    health_status: ProviderState
    last_success_at: Optional[str] = None
    last_failure_at: Optional[str] = None
    failure_count: int = 0
    last_error: Optional[str] = None
    last_latency_ms: Optional[float] = None
    circuit_state: str = "CLOSED"


class AIRequest(BaseModel):
    request_id: str
    user_id: str
    role: str
    conversation_id: str
    concept_id: Optional[str] = None
    mode: str = "guided_learning"
    message: str
    conversation_history: List[Dict[str, str]] = Field(default_factory=list)
    learner_context: Dict[str, Any] = Field(default_factory=dict)
    timeout_seconds: float = 60.0
    created_at: str


class AIResponse(BaseModel):
    request_id: str
    conversation_id: str
    answer: str
    response_type: str = "guided_explanation"
    hints: List[str] = Field(default_factory=list)
    concept_id: Optional[str] = None
    requires_follow_up: bool = False
    provider: str
    model: str
    is_fallback: bool = False
    fallback_reason: Optional[str] = None
    latency_ms: float = 0.0
    tokens_used: Optional[int] = None
    validation_status: str = "VERIFIED"
    state: OrchestratorState = OrchestratorState.COMPLETED

