"""
SUTRA LEARN — Ollama Local Models Transport & Adapters
Implements dedicated adapters for Qwen 3.5 4B (qwen3.5:4b) and Gemma 4 E2B (gemma4:e2b),
managing Ollama connectivity, bounded context, and reasoning stream extraction.
"""

import time
import logging
from typing import Dict, Any, List, Optional
import httpx

from app.ai.models import ErrorCategory, ProviderType
from app.ai.config import AISettings
from app.ai.curriculum_context import get_grounded_concept_context

logger = logging.getLogger("sutra.ai.ollama_adapters")


class OllamaTransport:
    """Shared low-level HTTP transport layer for Ollama."""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self._cached_tags: List[str] = []
        self._last_tag_check: float = 0.0

    async def get_installed_models(self, cache_seconds: float = 30.0) -> List[str]:
        now = time.time()
        if self._cached_tags and (now - self._last_tag_check < cache_seconds):
            return self._cached_tags

        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                res = await client.get(f"{self.base_url}/api/tags")
                if res.status_code == 200:
                    models = res.json().get("models", [])
                    names = [m.get("name") for m in models if m.get("name")]
                    self._cached_tags = names
                    self._last_tag_check = now
                    return names
        except Exception as e:
            logger.debug(f"Ollama tags query failed: {e}")
            pass
        return self._cached_tags

    async def chat(
        self,
        model: str,
        messages: List[Dict[str, str]],
        options: Dict[str, Any],
        timeout_seconds: float
    ) -> Dict[str, Any]:
        """Executes a multi-turn chat request against Ollama."""
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": options
        }
        async with httpx.AsyncClient(timeout=timeout_seconds) as client:
            res = await client.post(url, json=payload)
            if res.status_code != 200:
                raise OllamaException(
                    ErrorCategory.SDK_ERROR,
                    f"Ollama returned HTTP {res.status_code}: {res.text}"
                )
            return res.json()


class QwenAdapter:
    """Adapter for Qwen 3.5 4B (qwen3.5:4b)."""

    def __init__(self, settings: AISettings, transport: OllamaTransport):
        self.settings = settings
        self.transport = transport
        self.provider_id = "ollama_qwen"
        self.display_name = "Qwen 3.5 4B (Local)"
        self.provider_type = ProviderType.OLLAMA_QWEN
        self.model_id = settings.ollama_qwen_model

    async def is_available(self) -> bool:
        installed = await self.transport.get_installed_models(self.settings.ai_provider_health_cache_seconds)
        return self.model_id in installed

    async def generate_tutor_response(
        self,
        message: str,
        concept_id: Optional[str],
        mode: str,
        conversation_history: List[Dict[str, str]],
        learner_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        grounding = get_grounded_concept_context(concept_id or "MATH-C01")
        concept_title = grounding.get("title", "Linear Equations")

        system_msg = (
            f"You are SUTRA AI, a Class 8 NCERT Mathematics tutor. "
            f"Teaching Mode: {mode}. Concept: {concept_title}. "
            f"Provide a clear, pedagogical response explaining the mathematical steps. "
            f"Never give raw answers without steps. Always verify LHS = RHS."
        )

        messages = [{"role": "system", "content": system_msg}]
        for m in conversation_history[-6:]:
            role = "user" if m.get("sender_role") == "user" else "assistant"
            messages.append({"role": role, "content": m.get("content", "")})
        messages.append({"role": "user", "content": message})

        options = {
            "temperature": self.settings.qwen_temperature,
            "top_p": self.settings.qwen_top_p,
            "num_predict": self.settings.qwen_max_output_tokens
        }

        start = time.time()
        try:
            data = await self.transport.chat(
                model=self.model_id,
                messages=messages,
                options=options,
                timeout_seconds=self.settings.qwen_timeout_seconds
            )
            latency_ms = round((time.time() - start) * 1000, 2)
            msg_obj = data.get("message", {})
            content = msg_obj.get("content", "").strip()

            # If content is empty but model produced output in thinking
            if not content and msg_obj.get("thinking"):
                # Clean reasoning output as fallback
                content = msg_obj.get("thinking").strip()

            if not content:
                raise OllamaException(ErrorCategory.EMPTY_RESPONSE, "Qwen produced an empty response.")

            resp_type = "guided_explanation"
            if mode == "worked_example":
                resp_type = "worked_example"
            elif mode == "practice":
                resp_type = "practice_question"

            eval_count = data.get("eval_count")

            return {
                "answer": content,
                "response_type": resp_type,
                "hints": [
                    "Remember to balance the equation by performing operations on both sides.",
                    "Check your work by substituting the solution back into the original equation."
                ],
                "concept_id": concept_id or "MATH-C01",
                "requires_follow_up": True,
                "provider": "Ollama (Qwen)",
                "model": self.model_id,
                "is_fallback": False,
                "fallback_reason": None,
                "latency_ms": latency_ms,
                "tokens_used": eval_count
            }
        except httpx.TimeoutException:
            latency_ms = round((time.time() - start) * 1000, 2)
            raise OllamaException(ErrorCategory.TIMEOUT, f"Qwen inference timed out after {self.settings.qwen_timeout_seconds}s", latency_ms)
        except Exception as e:
            latency_ms = round((time.time() - start) * 1000, 2)
            if isinstance(e, OllamaException):
                raise
            raise OllamaException(ErrorCategory.SDK_ERROR, str(e), latency_ms)


class GemmaAdapter:
    """Adapter for Gemma 4 E2B (gemma4:e2b)."""

    def __init__(self, settings: AISettings, transport: OllamaTransport):
        self.settings = settings
        self.transport = transport
        self.provider_id = "ollama_gemma"
        self.display_name = "Gemma 4 E2B (Local)"
        self.provider_type = ProviderType.OLLAMA_GEMMA
        self.model_id = settings.ollama_gemma_model

    async def is_available(self) -> bool:
        installed = await self.transport.get_installed_models(self.settings.ai_provider_health_cache_seconds)
        return self.model_id in installed

    async def generate_tutor_response(
        self,
        message: str,
        concept_id: Optional[str],
        mode: str,
        conversation_history: List[Dict[str, str]],
        learner_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        grounding = get_grounded_concept_context(concept_id or "MATH-C01")
        concept_title = grounding.get("title", "Linear Equations")

        system_msg = (
            f"You are SUTRA AI, a Class 8 NCERT Mathematics tutor. "
            f"Teaching Mode: {mode}. Concept: {concept_title}. "
            f"Provide a clear, pedagogical response explaining the mathematical steps. "
            f"Never give raw answers without steps. Always verify LHS = RHS."
        )

        messages = [{"role": "system", "content": system_msg}]
        for m in conversation_history[-6:]:
            role = "user" if m.get("sender_role") == "user" else "assistant"
            messages.append({"role": role, "content": m.get("content", "")})
        messages.append({"role": "user", "content": message})

        options = {
            "temperature": self.settings.gemma_temperature,
            "top_p": self.settings.gemma_top_p,
            "num_predict": self.settings.gemma_max_output_tokens
        }

        start = time.time()
        try:
            data = await self.transport.chat(
                model=self.model_id,
                messages=messages,
                options=options,
                timeout_seconds=self.settings.gemma_timeout_seconds
            )
            latency_ms = round((time.time() - start) * 1000, 2)
            content = data.get("message", {}).get("content", "").strip()

            if not content:
                raise OllamaException(ErrorCategory.EMPTY_RESPONSE, "Gemma produced an empty response.")

            resp_type = "guided_explanation"
            if mode == "worked_example":
                resp_type = "worked_example"
            elif mode == "practice":
                resp_type = "practice_question"

            eval_count = data.get("eval_count")

            return {
                "answer": content,
                "response_type": resp_type,
                "hints": [
                    "Perform the inverse operation to isolate the variable term.",
                    "Verify your calculation by evaluating the equation with your answer."
                ],
                "concept_id": concept_id or "MATH-C01",
                "requires_follow_up": True,
                "provider": "Ollama (Gemma)",
                "model": self.model_id,
                "is_fallback": True,
                "fallback_reason": "Serving from local Gemma 4 E2B model",
                "latency_ms": latency_ms,
                "tokens_used": eval_count
            }
        except httpx.TimeoutException:
            latency_ms = round((time.time() - start) * 1000, 2)
            raise OllamaException(ErrorCategory.TIMEOUT, f"Gemma inference timed out after {self.settings.gemma_timeout_seconds}s", latency_ms)
        except Exception as e:
            latency_ms = round((time.time() - start) * 1000, 2)
            if isinstance(e, OllamaException):
                raise
            raise OllamaException(ErrorCategory.SDK_ERROR, str(e), latency_ms)


class OllamaException(Exception):
    def __init__(self, category: ErrorCategory, message: str, latency_ms: float = 0.0):
        super().__init__(message)
        self.category = category
        self.message = message
        self.latency_ms = latency_ms

