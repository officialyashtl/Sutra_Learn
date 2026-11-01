"""
SUTRA LEARN — AI Circuit Breaker Implementation
Prevents retry storms, isolates provider outages, and manages cooldown recovery probes.
"""

import time
import logging
from typing import Dict, Any, Optional
from app.ai.models import ErrorCategory

logger = logging.getLogger("sutra.ai.circuit_breaker")


class CircuitBreaker:
    def __init__(
        self,
        provider_id: str,
        failure_threshold: int = 3,
        cooldown_seconds: float = 30.0
    ):
        self.provider_id = provider_id
        self.failure_threshold = failure_threshold
        self.cooldown_seconds = cooldown_seconds
        
        self.state: str = "CLOSED"  # CLOSED | OPEN | HALF_OPEN
        self.failure_count: int = 0
        self.last_failure_time: float = 0.0
        self.last_success_time: float = 0.0
        self.last_error: Optional[str] = None
        self.last_error_category: Optional[ErrorCategory] = None

    def can_attempt(self) -> bool:
        """Determines if requests are permitted to reach the provider."""
        now = time.time()
        if self.state == "CLOSED":
            return True

        if self.state == "OPEN":
            # Check if cooldown has elapsed
            if now - self.last_failure_time >= self.cooldown_seconds:
                logger.info(f"Circuit Breaker [{self.provider_id}]: Cooldown expired ({self.cooldown_seconds}s). Transitioning OPEN -> HALF_OPEN.")
                self.state = "HALF_OPEN"
                return True
            return False

        if self.state == "HALF_OPEN":
            # Allow a single exploratory request
            return True

        return False

    def record_success(self) -> None:
        """Records a successful response and resets failure counters."""
        now = time.time()
        self.last_success_time = now
        self.failure_count = 0
        self.last_error = None
        self.last_error_category = None
        if self.state != "CLOSED":
            logger.info(f"Circuit Breaker [{self.provider_id}]: Successful response received. Transitioning {self.state} -> CLOSED.")
            self.state = "CLOSED"

    def record_failure(self, category: ErrorCategory, error_msg: str) -> None:
        """Records a failure and conditionally trips the circuit."""
        now = time.time()
        self.last_failure_time = now
        self.last_error = error_msg
        self.last_error_category = category
        self.failure_count += 1

        # Permanent errors immediately trip the breaker
        if category in (ErrorCategory.PERMISSION_DENIED, ErrorCategory.PERMANENT_AUTH, ErrorCategory.MODEL_NOT_FOUND):
            logger.warning(
                f"Circuit Breaker [{self.provider_id}]: Permanent error ({category.value}) detected: {error_msg}. "
                f"Immediately tripping circuit to OPEN."
            )
            self.state = "OPEN"
            return

        if self.state == "HALF_OPEN":
            logger.warning(f"Circuit Breaker [{self.provider_id}]: Probe failed in HALF_OPEN. Tripping back to OPEN.")
            self.state = "OPEN"
            return

        if self.failure_count >= self.failure_threshold:
            logger.warning(
                f"Circuit Breaker [{self.provider_id}]: Failure threshold reached ({self.failure_count}/{self.failure_threshold}). "
                f"Tripping circuit CLOSED -> OPEN for {self.cooldown_seconds}s."
            )
            self.state = "OPEN"

    def get_status(self) -> Dict[str, Any]:
        return {
            "provider_id": self.provider_id,
            "state": self.state,
            "failure_count": self.failure_count,
            "cooldown_seconds": self.cooldown_seconds,
            "seconds_since_last_failure": (time.time() - self.last_failure_time) if self.last_failure_time > 0 else None,
            "last_error": self.last_error,
            "last_error_category": self.last_error_category.value if self.last_error_category else None
        }

