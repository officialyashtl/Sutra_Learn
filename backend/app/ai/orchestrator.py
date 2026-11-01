"""
SUTRA LEARN — AI Orchestrator & State Machine
Executes the 12-state request lifecycle, manages multi-provider cascade,
enforces mathematical validation, circuit breaker recording, and request traceability.
"""

import uuid
import time
import random
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

from app.ai.models import OrchestratorState, ErrorCategory, AIRequest, AIResponse
from app.ai.config import AISettings, get_ai_settings
from app.ai.registry import AIProviderRegistry, get_ai_registry
from app.ai.math_validator import MathematicalValidator
from app.ai.gemini_adapter import GeminiAPIException
from app.ai.ollama_adapters import OllamaException

logger = logging.getLogger("sutra.ai.orchestrator")


class AIOrchestrator:
    def __init__(self, registry: Optional[AIProviderRegistry] = None, settings: Optional[AISettings] = None):
        self.settings = settings or get_ai_settings()
        self.registry = registry or get_ai_registry()
        # Fallback provider import avoided at module level to prevent circular dependency
        self._fallback_provider = None

    @property
    def fallback_provider(self):
        if self._fallback_provider is None:
            from app.ai.provider import CurriculumGroundedFallbackProvider
            self._fallback_provider = CurriculumGroundedFallbackProvider()
        return self._fallback_provider

    async def execute_tutor_request(
        self,
        user_id: str,
        role: str,
        message: str,
        conversation_id: str,
        concept_id: Optional[str] = None,
        mode: str = "guided_learning",
        conversation_history: Optional[List[Dict[str, str]]] = None,
        learner_context: Optional[Dict[str, Any]] = None
    ) -> AIResponse:
        """
        Orchestrates an authenticated student request through the full 12-state lifecycle.
        """
        request_id = f"req_{uuid.uuid4().hex[:12]}"
        now_iso = datetime.now(timezone.utc).isoformat()
        start_time = time.time()

        req = AIRequest(
            request_id=request_id,
            user_id=user_id,
            role=role,
            conversation_id=conversation_id,
            concept_id=concept_id,
            mode=mode,
            message=message,
            conversation_history=conversation_history or [],
            learner_context=learner_context or {},
            timeout_seconds=self.settings.ai_request_timeout_seconds,
            created_at=now_iso
        )

        # STATE: RECEIVED
        logger.info(f"[{request_id}] State: RECEIVED | User: {user_id} | Mode: {mode} | Concept: {concept_id}")

        # STATE: VALIDATING
        if len(req.message) > self.settings.ai_max_user_input_chars:
            logger.warning(f"[{request_id}] Input message exceeded max chars ({len(req.message)} > {self.settings.ai_max_user_input_chars})")
            req.message = req.message[:self.settings.ai_max_user_input_chars]

        # STATE: AUTHORIZING
        if self.settings.ai_require_auth and not user_id:
            logger.error(f"[{request_id}] Unauthorized AI request attempted.")
            raise PermissionError("Authentication required for AI Tutor interaction.")

        # STATE: BUILDING_CONTEXT
        # Truncate history to bounded limits
        bounded_history = req.conversation_history[-self.settings.ai_max_history_messages:]

        # STATE: SELECTING_PROVIDER
        eligible_providers = await self.registry.get_eligible_providers()
        logger.info(f"[{request_id}] Eligible providers: {[p.provider_id for p in eligible_providers]}")

        final_response: Optional[Dict[str, Any]] = None
        attempt_count = 0
        fallback_reasons: List[str] = []

        for provider in eligible_providers:
            if attempt_count >= self.settings.ai_max_total_attempts:
                break
            attempt_count += 1
            provider_id = provider.provider_id
            cb = self.registry.get_circuit_breaker(provider_id)

            logger.info(f"[{request_id}] State: GENERATING via {provider.display_name} ({provider.model_id})")
            try:
                raw_res = await provider.generate_tutor_response(
                    message=req.message,
                    concept_id=req.concept_id,
                    mode=req.mode,
                    conversation_history=bounded_history,
                    learner_context=req.learner_context
                )
                cb.record_success()

                # STATE: VALIDATING_OUTPUT
                answer_text = raw_res.get("answer", "")
                math_val = MathematicalValidator.validate_step_consistency(answer_text)
                if not math_val["valid"]:
                    logger.warning(
                        f"[{request_id}] Mathematical step validation failure: {math_val.get('reason')}. "
                        f"Attempting fallback provider."
                    )
                    fallback_reasons.append(f"{provider.display_name} output failed algebraic validation: {math_val.get('reason')}")
                    continue

                final_response = raw_res
                final_response["validation_status"] = "VERIFIED"
                break

            except GeminiAPIException as ge:
                cb.record_failure(ge.category, ge.message)
                reason = f"Gemini API failure ({ge.category.value}): {ge.message}"
                fallback_reasons.append(reason)
                logger.warning(f"[{request_id}] {reason}")

            except OllamaException as oe:
                cb.record_failure(oe.category, oe.message)
                reason = f"Ollama {provider.display_name} failure ({oe.category.value}): {oe.message}"
                fallback_reasons.append(reason)
                logger.warning(f"[{request_id}] {reason}")

            except Exception as e:
                cb.record_failure(ErrorCategory.UNKNOWN, str(e))
                reason = f"Provider {provider_id} unexpected failure: {str(e)}"
                fallback_reasons.append(reason)
                logger.warning(f"[{request_id}] {reason}")

        # STATE: FALLBACK (if models were unavailable or failed validation)
        if not final_response:
            logger.info(f"[{request_id}] State: FALLBACK to Curriculum Grounded Deterministic Engine.")
            reason_summary = " | ".join(fallback_reasons) if fallback_reasons else "Operating mode or provider availability routed to curriculum engine"
            fallback_res = await self.fallback_provider.generate_tutor_response(
                message=req.message,
                concept_id=req.concept_id,
                mode=req.mode,
                conversation_history=bounded_history,
                learner_context=req.learner_context
            )
            fallback_res["is_fallback"] = True
            fallback_res["fallback_reason"] = reason_summary
            fallback_res["provider"] = "NCERT Curriculum Engine"
            fallback_res["model"] = "curriculum_fallback"
            fallback_res["validation_status"] = "CURRICULUM_VERIFIED"
            final_response = fallback_res

        total_latency_ms = round((time.time() - start_time) * 1000, 2)
        final_response["latency_ms"] = total_latency_ms
        final_response["request_id"] = request_id

        # STATE: COMPLETED
        logger.info(
            f"[{request_id}] State: COMPLETED | Provider: {final_response.get('provider')} "
            f"| Model: {final_response.get('model')} | Latency: {total_latency_ms}ms"
        )

        return AIResponse(
            request_id=request_id,
            conversation_id=conversation_id,
            answer=final_response["answer"],
            response_type=final_response.get("response_type", "guided_explanation"),
            hints=final_response.get("hints", []),
            concept_id=final_response.get("concept_id", req.concept_id),
            requires_follow_up=final_response.get("requires_follow_up", True),
            provider=final_response["provider"],
            model=final_response["model"],
            is_fallback=final_response.get("is_fallback", False),
            fallback_reason=final_response.get("fallback_reason"),
            latency_ms=total_latency_ms,
            tokens_used=final_response.get("tokens_used"),
            validation_status=final_response.get("validation_status", "VERIFIED"),
            state=OrchestratorState.COMPLETED
        )


# Singleton orchestrator
_orchestrator: Optional[AIOrchestrator] = None


def get_ai_orchestrator() -> AIOrchestrator:
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = AIOrchestrator()
    return _orchestrator

