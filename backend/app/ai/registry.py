"""
SUTRA LEARN — AI Provider Registry & Lifecycle Manager
Manages provider instances, circuit breakers, health evaluations, and policy-based provider selection.
"""

import time
import logging
from typing import Dict, Any, List, Optional

from app.ai.models import ProviderType, ProviderState, ProviderHealth, ErrorCategory
from app.ai.config import AISettings, get_ai_settings
from app.ai.circuit_breaker import CircuitBreaker
from app.ai.gemini_adapter import GeminiAdapter
from app.ai.ollama_adapters import OllamaTransport, QwenAdapter, GemmaAdapter

logger = logging.getLogger("sutra.ai.registry")


class AIProviderRegistry:
    def __init__(self, settings: Optional[AISettings] = None):
        self.settings = settings or get_ai_settings()
        
        # Shared Ollama transport
        self.ollama_transport = OllamaTransport(self.settings.ollama_base_url)

        # Adapters
        self.gemini = GeminiAdapter(self.settings)
        self.qwen = QwenAdapter(self.settings, self.ollama_transport)
        self.gemma = GemmaAdapter(self.settings, self.ollama_transport)

        # Circuit breakers
        self.circuit_breakers: Dict[str, CircuitBreaker] = {
            "gemini": CircuitBreaker(
                "gemini",
                failure_threshold=self.settings.ai_circuit_breaker_failure_threshold,
                cooldown_seconds=self.settings.ai_circuit_breaker_cooldown_seconds
            ),
            "ollama_qwen": CircuitBreaker(
                "ollama_qwen",
                failure_threshold=self.settings.ai_circuit_breaker_failure_threshold,
                cooldown_seconds=self.settings.ai_circuit_breaker_cooldown_seconds
            ),
            "ollama_gemma": CircuitBreaker(
                "ollama_gemma",
                failure_threshold=self.settings.ai_circuit_breaker_failure_threshold,
                cooldown_seconds=self.settings.ai_circuit_breaker_cooldown_seconds
            ),
            "deterministic": CircuitBreaker("deterministic", failure_threshold=999, cooldown_seconds=0)
        }

        # Cached health
        self._cached_health: Optional[List[ProviderHealth]] = None
        self._last_health_check: float = 0.0

    def get_circuit_breaker(self, provider_id: str) -> CircuitBreaker:
        return self.circuit_breakers.get(provider_id) or self.circuit_breakers["deterministic"]

    async def get_eligible_providers(self, mode: Optional[str] = None) -> List[Any]:
        """
        Determines the ordered list of eligible provider adapters based on operating mode,
        activation flags, circuit breaker status, and local model availability.
        """
        if self.settings.app_env == "testing":
            # Fast deterministic testing path
            return []

        op_mode = (mode or self.settings.ai_mode).lower()
        eligible = []

        # 1. Gemini
        can_use_gemini = (
            op_mode in ("auto", "cloud")
            and not self.settings.ai_offline_mode
            and self.settings.ai_enable_gemini
            and self.gemini.is_configured()
            and self.circuit_breakers["gemini"].can_attempt()
        )
        if can_use_gemini:
            eligible.append(self.gemini)

        # 2. Qwen
        can_use_qwen = (
            op_mode in ("auto", "local", "offline")
            and self.settings.ai_enable_qwen
            and self.circuit_breakers["ollama_qwen"].can_attempt()
        )
        if can_use_qwen and await self.qwen.is_available():
            eligible.append(self.qwen)

        # 3. Gemma
        can_use_gemma = (
            op_mode in ("auto", "local", "offline")
            and self.settings.ai_enable_gemma
            and self.circuit_breakers["ollama_gemma"].can_attempt()
        )
        if can_use_gemma and await self.gemma.is_available():
            eligible.append(self.gemma)

        return eligible

    async def evaluate_provider_health(self) -> List[ProviderHealth]:
        """Performs non-invasive health evaluation across all registered providers."""
        now = time.time()
        if self._cached_health and (now - self._last_health_check < self.settings.ai_provider_health_cache_seconds):
            return self._cached_health

        health_list = []

        # Gemini
        cb_gemini = self.circuit_breakers["gemini"]
        gem_state = ProviderState.AVAILABLE
        if not self.gemini.is_configured():
            gem_state = ProviderState.NOT_CONFIGURED
        elif not self.settings.ai_enable_gemini or self.settings.ai_offline_mode:
            gem_state = ProviderState.DISABLED
        elif cb_gemini.state == "OPEN":
            gem_state = ProviderState.CIRCUIT_OPEN
        elif cb_gemini.failure_count > 0:
            gem_state = ProviderState.DEGRADED

        health_list.append(ProviderHealth(
            provider_id="gemini",
            display_name=self.gemini.display_name,
            provider_type=ProviderType.GEMINI,
            configured=self.gemini.is_configured(),
            enabled=self.settings.ai_enable_gemini and not self.settings.ai_offline_mode,
            model_id=self.gemini.model_id,
            health_status=gem_state,
            failure_count=cb_gemini.failure_count,
            last_error=cb_gemini.last_error,
            circuit_state=cb_gemini.state
        ))

        # Ollama models query
        installed = await self.ollama_transport.get_installed_models(self.settings.ai_provider_health_cache_seconds)
        ollama_reachable = len(installed) > 0

        # Qwen
        cb_qwen = self.circuit_breakers["ollama_qwen"]
        qwen_installed = self.qwen.model_id in installed
        qwen_state = ProviderState.AVAILABLE
        if not ollama_reachable or not qwen_installed:
            qwen_state = ProviderState.UNAVAILABLE
        elif not self.settings.ai_enable_qwen:
            qwen_state = ProviderState.DISABLED
        elif cb_qwen.state == "OPEN":
            qwen_state = ProviderState.CIRCUIT_OPEN
        elif cb_qwen.failure_count > 0:
            qwen_state = ProviderState.DEGRADED

        health_list.append(ProviderHealth(
            provider_id="ollama_qwen",
            display_name=self.qwen.display_name,
            provider_type=ProviderType.OLLAMA_QWEN,
            configured=qwen_installed,
            enabled=self.settings.ai_enable_qwen,
            model_id=self.qwen.model_id,
            health_status=qwen_state,
            failure_count=cb_qwen.failure_count,
            last_error=cb_qwen.last_error,
            circuit_state=cb_qwen.state
        ))

        # Gemma
        cb_gemma = self.circuit_breakers["ollama_gemma"]
        gemma_installed = self.gemma.model_id in installed
        gemma_state = ProviderState.AVAILABLE
        if not ollama_reachable or not gemma_installed:
            gemma_state = ProviderState.UNAVAILABLE
        elif not self.settings.ai_enable_gemma:
            gemma_state = ProviderState.DISABLED
        elif cb_gemma.state == "OPEN":
            gemma_state = ProviderState.CIRCUIT_OPEN
        elif cb_gemma.failure_count > 0:
            gemma_state = ProviderState.DEGRADED

        health_list.append(ProviderHealth(
            provider_id="ollama_gemma",
            display_name=self.gemma.display_name,
            provider_type=ProviderType.OLLAMA_GEMMA,
            configured=gemma_installed,
            enabled=self.settings.ai_enable_gemma,
            model_id=self.gemma.model_id,
            health_status=gemma_state,
            failure_count=cb_gemma.failure_count,
            last_error=cb_gemma.last_error,
            circuit_state=cb_gemma.state
        ))

        # Deterministic Fallback Engine
        health_list.append(ProviderHealth(
            provider_id="deterministic",
            display_name="NCERT Curriculum Fallback Engine",
            provider_type=ProviderType.DETERMINISTIC,
            configured=True,
            enabled=True,
            model_id="curriculum_fallback",
            health_status=ProviderState.AVAILABLE,
            failure_count=0,
            circuit_state="CLOSED"
        ))

        self._cached_health = health_list
        self._last_health_check = now
        return health_list


# Singleton registry instance
_registry: Optional[AIProviderRegistry] = None


def get_ai_registry() -> AIProviderRegistry:
    global _registry
    if _registry is None:
        _registry = AIProviderRegistry()
    return _registry

