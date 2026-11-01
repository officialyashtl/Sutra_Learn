"""
SUTRA LEARN — Official Google Gemini API Provider Adapter
Utilizes the official google-genai SDK with full async support, precise error classification,
and system instructions grounded in NCERT Class 8 Mathematics.
"""

import time
import logging
from typing import Dict, Any, List, Optional

from app.ai.models import ErrorCategory, ProviderType
from app.ai.config import AISettings
from app.ai.curriculum_context import get_grounded_concept_context

logger = logging.getLogger("sutra.ai.gemini_adapter")


class GeminiAdapter:
    def __init__(self, settings: AISettings):
        self.settings = settings
        self.provider_id = "gemini"
        self.display_name = "Google Gemini API"
        self.provider_type = ProviderType.GEMINI
        self.model_id = settings.gemini_model
        self.api_key = settings.gemini_api_key
        self._client = None

        if self.api_key and not self.api_key.startswith("mock") and not self.api_key.startswith("your_"):
            try:
                from google import genai
                self._client = genai.Client(api_key=self.api_key)
            except Exception as e:
                logger.error(f"Failed to initialize Google GenAI client: {e}")
                self._client = None

    def is_configured(self) -> bool:
        return self._client is not None and bool(self.api_key)

    async def generate_tutor_response(
        self,
        message: str,
        concept_id: Optional[str],
        mode: str,
        conversation_history: List[Dict[str, str]],
        learner_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Invokes Gemini using official SDK with complete error classification."""
        if not self.is_configured():
            raise ValueError("Gemini provider is not configured with a valid API key.")

        grounding = get_grounded_concept_context(concept_id or "MATH-C01")
        concept_title = grounding.get("title", "Linear Equations")
        lesson_obj = grounding.get("lesson") or {}
        concept_core = lesson_obj.get("objective", "") if isinstance(lesson_obj, dict) else str(lesson_obj)

        system_instruction = (
            f"You are SUTRA AI, an elite mathematics tutor specializing in NCERT Class 8 Mathematics.\n"
            f"Concept: {concept_title}.\n"
            f"Curriculum Core: {concept_core}\n"
            f"Teaching Mode: {mode}.\n"
            f"Pedagogical Rules:\n"
            f"1. Never give raw answers directly without showing the step-by-step mathematical reasoning.\n"
            f"2. Emphasize balance operations: whatever is done to one side must be done to the other.\n"
            f"3. Maintain warm, encouraging, Earthbound Editorial tone.\n"
            f"4. Provide 1 to 2 progressive hints for the student.\n"
        )

        prompt_parts = []
        if conversation_history:
            prompt_parts.append("Previous Conversation:")
            for msg in conversation_history[-6:]:
                role = "Student" if msg.get("sender_role") == "user" else "Tutor"
                prompt_parts.append(f"{role}: {msg.get('content', '')}")
            prompt_parts.append("\nCurrent Question:")

        prompt_parts.append(f"Student: {message}")
        full_prompt = "\n".join(prompt_parts)

        start_time = time.time()
        try:
            from google.genai import types

            config = types.GenerateContentConfig(
                temperature=self.settings.gemini_temperature,
                max_output_tokens=self.settings.gemini_max_output_tokens,
                system_instruction=system_instruction
            )

            # Async call via client.aio
            response = await self._client.aio.models.generate_content(
                model=self.model_id,
                contents=full_prompt,
                config=config
            )

            latency_ms = round((time.time() - start_time) * 1000, 2)
            answer_text = response.text.strip() if response.text else ""

            if not answer_text:
                raise ValueError("Empty generation received from Gemini API.")

            tokens = None
            if hasattr(response, "usage_metadata") and response.usage_metadata:
                tokens = getattr(response.usage_metadata, "total_token_count", None)

            resp_type = "guided_explanation"
            if mode == "worked_example":
                resp_type = "worked_example"
            elif mode == "practice":
                resp_type = "practice_question"

            return {
                "answer": answer_text,
                "response_type": resp_type,
                "hints": [
                    "Check both sides of the equation after applying the operation.",
                    "Verify your answer by substituting the value back into the original equation."
                ],
                "concept_id": concept_id or "MATH-C01",
                "requires_follow_up": True,
                "provider": "Google Gemini",
                "model": self.model_id,
                "is_fallback": False,
                "fallback_reason": None,
                "latency_ms": latency_ms,
                "tokens_used": tokens
            }

        except Exception as e:
            latency_ms = round((time.time() - start_time) * 1000, 2)
            category = self.classify_error(e)
            logger.warning(f"Gemini API invocation failed ({category.value}): {e}")
            raise GeminiAPIException(category, str(e), latency_ms)

    def classify_error(self, e: Exception) -> ErrorCategory:
        """Categorizes raw exceptions into defined failure categories."""
        err_str = str(e).lower()
        if "403" in err_str or "permission_denied" in err_str or "billing" in err_str:
            return ErrorCategory.PERMISSION_DENIED
        if "401" in err_str or "unauthenticated" in err_str or "invalid api key" in err_str:
            return ErrorCategory.PERMANENT_AUTH
        if "404" in err_str or "not_found" in err_str or "is not found" in err_str:
            return ErrorCategory.MODEL_NOT_FOUND
        if "429" in err_str or "quota" in err_str or "resource_exhausted" in err_str:
            return ErrorCategory.QUOTA_EXCEEDED
        if "timeout" in err_str or "timed out" in err_str:
            return ErrorCategory.TIMEOUT
        if "safety" in err_str or "blocked" in err_str:
            return ErrorCategory.SAFETY_REJECTION
        if "empty" in err_str:
            return ErrorCategory.EMPTY_RESPONSE
        return ErrorCategory.SDK_ERROR


class GeminiAPIException(Exception):
    def __init__(self, category: ErrorCategory, message: str, latency_ms: float):
        super().__init__(message)
        self.category = category
        self.message = message
        self.latency_ms = latency_ms
