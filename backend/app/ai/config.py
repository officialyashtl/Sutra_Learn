"""
SUTRA LEARN — Centralized AI Infrastructure Configuration
Version: 1.0.0 (AI Ascension 1000)
Validates all environment variables, provider activation flags, timeouts,
retry parameters, circuit breakers, and security boundaries using Pydantic Settings.
"""

import os
from typing import Literal, Optional
from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AISettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # -------------------------------------------------------------------------
    # Application Environment
    # -------------------------------------------------------------------------
    app_env: Literal["development", "testing", "staging", "production"] = Field(
        default="development",
        alias="APP_ENV",
        description="Deployment stage; production enforces strict security"
    )
    app_debug: bool = Field(
        default=False,
        alias="APP_DEBUG",
        description="Verbose debugging flag; must be false in production"
    )
    app_timezone: str = Field(
        default="Asia/Kolkata",
        alias="APP_TIMEZONE",
        description="Standard time zone for analytics and audit trails"
    )

    # -------------------------------------------------------------------------
    # AI Operating Mode
    # -------------------------------------------------------------------------
    ai_mode: Literal["auto", "cloud", "local", "offline"] = Field(
        default="auto",
        alias="AI_MODE",
        description="auto: cascade all available | cloud: cloud only | local: local only | offline: strictly no network"
    )
    ai_primary_provider: str = Field(
        default="gemini",
        alias="AI_PRIMARY_PROVIDER",
        description="Preferred top-priority provider in auto mode"
    )
    ai_offline_mode: bool = Field(
        default=False,
        alias="AI_OFFLINE_MODE",
        description="When true, prohibits any outbound network calls to cloud providers"
    )
    ai_enable_fallback: bool = Field(
        default=True,
        alias="AI_ENABLE_FALLBACK",
        description="Allows automatic cascade to secondary/deterministic providers"
    )
    ai_enable_deterministic: bool = Field(
        default=True,
        alias="AI_ENABLE_DETERMINISTIC",
        description="Ensures curriculum-grounded deterministic engine is always available"
    )

    # -------------------------------------------------------------------------
    # Provider Activation
    # -------------------------------------------------------------------------
    ai_enable_gemini: bool = Field(default=True, alias="AI_ENABLE_GEMINI")
    ai_enable_qwen: bool = Field(default=True, alias="AI_ENABLE_QWEN")
    ai_enable_gemma: bool = Field(default=True, alias="AI_ENABLE_GEMMA")

    # -------------------------------------------------------------------------
    # Google Gemini Configuration
    # -------------------------------------------------------------------------
    gemini_api_key: Optional[str] = Field(
        default=None,
        alias="GEMINI_API_KEY",
        description="Google Gemini API Secret Key"
    )
    gemini_model: str = Field(
        default="gemini-3.8-flash",
        alias="GEMINI_MODEL",
        description="Verified generation-compatible Gemini model identifier"
    )
    gemini_timeout_seconds: float = Field(default=60.0, alias="GEMINI_TIMEOUT_SECONDS", ge=5.0, le=300.0)
    gemini_max_output_tokens: int = Field(default=2048, alias="GEMINI_MAX_OUTPUT_TOKENS", ge=128, le=8192)
    gemini_temperature: float = Field(default=0.3, alias="GEMINI_TEMPERATURE", ge=0.0, le=2.0)
    gemini_max_retries: int = Field(default=1, alias="GEMINI_MAX_RETRIES", ge=0, le=5)

    # -------------------------------------------------------------------------
    # Ollama Local Runtime Configuration
    # -------------------------------------------------------------------------
    ollama_base_url: str = Field(
        default="http://localhost:11434",
        alias="OLLAMA_BASE_URL",
        description="Localhost or secured private endpoint for Ollama runtime"
    )
    ollama_connect_timeout_seconds: float = Field(default=5.0, alias="OLLAMA_CONNECT_TIMEOUT_SECONDS", ge=1.0, le=30.0)
    ollama_read_timeout_seconds: float = Field(default=120.0, alias="OLLAMA_READ_TIMEOUT_SECONDS", ge=10.0, le=300.0)
    ollama_total_timeout_seconds: float = Field(default=180.0, alias="OLLAMA_TOTAL_TIMEOUT_SECONDS", ge=10.0, le=300.0)
    ollama_keep_alive: str = Field(default="5m", alias="OLLAMA_KEEP_ALIVE")
    ollama_num_parallel: int = Field(default=1, alias="OLLAMA_NUM_PARALLEL", ge=1, le=8)
    ollama_max_queue: int = Field(default=2, alias="OLLAMA_MAX_QUEUE", ge=1, le=16)

    # -------------------------------------------------------------------------
    # Qwen 3.5 4B Configuration
    # -------------------------------------------------------------------------
    ollama_qwen_model: str = Field(default="qwen3.5:4b", alias="OLLAMA_QWEN_MODEL")
    qwen_temperature: float = Field(default=0.3, alias="QWEN_TEMPERATURE", ge=0.0, le=2.0)
    qwen_top_p: float = Field(default=0.8, alias="QWEN_TOP_P", ge=0.0, le=1.0)
    qwen_max_output_tokens: int = Field(default=2048, alias="QWEN_MAX_OUTPUT_TOKENS", ge=64, le=8192)
    qwen_timeout_seconds: float = Field(default=180.0, alias="QWEN_TIMEOUT_SECONDS", ge=10.0, le=300.0)
    qwen_max_retries: int = Field(default=0, alias="QWEN_MAX_RETRIES", ge=0, le=3)

    # -------------------------------------------------------------------------
    # Gemma 4 E2B Configuration
    # -------------------------------------------------------------------------
    ollama_gemma_model: str = Field(default="gemma4:e2b", alias="OLLAMA_GEMMA_MODEL")
    gemma_temperature: float = Field(default=0.3, alias="GEMMA_TEMPERATURE", ge=0.0, le=2.0)
    gemma_top_p: float = Field(default=0.8, alias="GEMMA_TOP_P", ge=0.0, le=1.0)
    gemma_max_output_tokens: int = Field(default=2048, alias="GEMMA_MAX_OUTPUT_TOKENS", ge=64, le=8192)
    gemma_timeout_seconds: float = Field(default=180.0, alias="GEMMA_TIMEOUT_SECONDS", ge=10.0, le=300.0)
    gemma_max_retries: int = Field(default=0, alias="GEMMA_MAX_RETRIES", ge=0, le=3)

    # -------------------------------------------------------------------------
    # Orchestrator & Bounded Limits
    # -------------------------------------------------------------------------
    ai_provider_health_cache_seconds: int = Field(default=30, alias="AI_PROVIDER_HEALTH_CACHE_SECONDS", ge=5, le=300)
    ai_circuit_breaker_failure_threshold: int = Field(default=3, alias="AI_CIRCUIT_BREAKER_FAILURE_THRESHOLD", ge=1, le=10)
    ai_circuit_breaker_cooldown_seconds: int = Field(default=30, alias="AI_CIRCUIT_BREAKER_COOLDOWN_SECONDS", ge=5, le=300)
    ai_max_total_attempts: int = Field(default=3, alias="AI_MAX_TOTAL_ATTEMPTS", ge=1, le=6)
    ai_max_fallback_depth: int = Field(default=3, alias="AI_MAX_FALLBACK_DEPTH", ge=1, le=5)
    ai_request_timeout_seconds: float = Field(default=180.0, alias="AI_REQUEST_TIMEOUT_SECONDS", ge=15.0, le=600.0)
    ai_max_context_chars: int = Field(default=24000, alias="AI_MAX_CONTEXT_CHARS", ge=1000, le=100000)
    ai_max_history_messages: int = Field(default=12, alias="AI_MAX_HISTORY_MESSAGES", ge=2, le=50)
    ai_max_user_input_chars: int = Field(default=8000, alias="AI_MAX_USER_INPUT_CHARS", ge=100, le=32000)
    ai_max_response_chars: int = Field(default=16000, alias="AI_MAX_RESPONSE_CHARS", ge=200, le=64000)

    # -------------------------------------------------------------------------
    # Retry & Reliability
    # -------------------------------------------------------------------------
    ai_retry_backoff_base_seconds: float = Field(default=1.0, alias="AI_RETRY_BACKOFF_BASE_SECONDS", ge=0.1, le=10.0)
    ai_retry_backoff_max_seconds: float = Field(default=5.0, alias="AI_RETRY_BACKOFF_MAX_SECONDS", ge=1.0, le=30.0)
    ai_retry_jitter: bool = Field(default=True, alias="AI_RETRY_JITTER")
    ai_provider_failure_threshold: int = Field(default=3, alias="AI_PROVIDER_FAILURE_THRESHOLD", ge=1, le=10)
    ai_provider_recovery_probe: bool = Field(default=True, alias="AI_PROVIDER_RECOVERY_PROBE")

    # -------------------------------------------------------------------------
    # Streaming
    # -------------------------------------------------------------------------
    ai_streaming_enabled: bool = Field(default=False, alias="AI_STREAMING_ENABLED")
    ai_stream_heartbeat_seconds: int = Field(default=15, alias="AI_STREAM_HEARTBEAT_SECONDS", ge=1, le=60)
    ai_stream_max_duration_seconds: int = Field(default=180, alias="AI_STREAM_MAX_DURATION_SECONDS", ge=10, le=600)

    # -------------------------------------------------------------------------
    # Observability (Never logs raw secrets)
    # -------------------------------------------------------------------------
    ai_log_provider_metadata: bool = Field(default=True, alias="AI_LOG_PROVIDER_METADATA")
    ai_log_prompts: bool = Field(default=False, alias="AI_LOG_PROMPTS")
    ai_log_responses: bool = Field(default=False, alias="AI_LOG_RESPONSES")
    ai_log_latency: bool = Field(default=True, alias="AI_LOG_LATENCY")
    ai_log_token_usage: bool = Field(default=True, alias="AI_LOG_TOKEN_USAGE")

    # -------------------------------------------------------------------------
    # Security Boundaries
    # -------------------------------------------------------------------------
    ai_require_auth: bool = Field(default=True, alias="AI_REQUIRE_AUTH")
    ai_enforce_owner_check: bool = Field(default=True, alias="AI_ENFORCE_OWNER_CHECK")
    ai_enforce_teacher_scope: bool = Field(default=True, alias="AI_ENFORCE_TEACHER_SCOPE")
    ai_allow_client_provider_override: bool = Field(default=False, alias="AI_ALLOW_CLIENT_PROVIDER_OVERRIDE")
    ai_allow_remote_ollama: bool = Field(default=False, alias="AI_ALLOW_REMOTE_OLLAMA")

    # -------------------------------------------------------------------------
    # Server-Side Rate Limits
    # -------------------------------------------------------------------------
    ai_student_requests_per_minute: int = Field(default=20, alias="AI_STUDENT_REQUESTS_PER_MINUTE", ge=1, le=120)
    ai_teacher_requests_per_minute: int = Field(default=20, alias="AI_TEACHER_REQUESTS_PER_MINUTE", ge=1, le=120)
    ai_health_requests_per_minute: int = Field(default=30, alias="AI_HEALTH_REQUESTS_PER_MINUTE", ge=1, le=240)

    # -------------------------------------------------------------------------
    # Cross-Field Validations
    # -------------------------------------------------------------------------
    @model_validator(mode="after")
    def validate_security_and_environment(self) -> "AISettings":
        # Production security assertion
        if self.app_env == "production" and self.app_debug:
            raise ValueError("APP_DEBUG must be False in production environments.")

        # Offline mode enforces no cloud providers
        if self.ai_offline_mode or self.ai_mode == "offline":
            self.ai_enable_gemini = False

        # Ollama remote endpoint check in production
        if self.app_env == "production" and not self.ai_allow_remote_ollama:
            url_lower = self.ollama_base_url.lower()
            if not ("localhost" in url_lower or "127.0.0.1" in url_lower):
                raise ValueError("Remote Ollama endpoints require explicit AI_ALLOW_REMOTE_OLLAMA=true in production.")

        # Timeout hierarchy
        if self.ai_request_timeout_seconds < self.gemini_timeout_seconds:
            self.ai_request_timeout_seconds = self.gemini_timeout_seconds + 10.0

        return self

    def get_safe_status(self) -> dict:
        """Returns non-sensitive configuration status for logging & health inspection."""
        return {
            "app_env": self.app_env,
            "ai_mode": self.ai_mode,
            "offline_mode": self.ai_offline_mode,
            "gemini": {
                "enabled": self.ai_enable_gemini,
                "configured": bool(self.gemini_api_key and not self.gemini_api_key.startswith("mock")),
                "model": self.gemini_model,
                "timeout_s": self.gemini_timeout_seconds
            },
            "ollama": {
                "base_url": self.ollama_base_url,
                "qwen_model": self.ollama_qwen_model,
                "qwen_enabled": self.ai_enable_qwen,
                "gemma_model": self.ollama_gemma_model,
                "gemma_enabled": self.ai_enable_gemma
            },
            "deterministic_fallback": self.ai_enable_deterministic,
            "security": {
                "require_auth": self.ai_require_auth,
                "enforce_owner": self.ai_enforce_owner_check,
                "enforce_teacher_scope": self.ai_enforce_teacher_scope,
                "client_override_allowed": self.ai_allow_client_provider_override
            }
        }

    def safe_dump(self) -> dict:
        """Alias for get_safe_status() providing redacted configuration inspection."""
        return self.get_safe_status()


# Singleton instance
_settings: Optional[AISettings] = None


def get_ai_settings() -> AISettings:
    global _settings
    if _settings is None:
        _settings = AISettings()
    return _settings


def reset_ai_settings() -> None:
    """Allows testing harnesses to reload settings after environment variable modifications."""
    global _settings
    _settings = None

