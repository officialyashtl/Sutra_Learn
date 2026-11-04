"""
SUTRA LEARN — In-Memory Sliding Window Rate Limiter
Guards sensitive authentication and AI inference endpoints against brute-force and quota abuse.
Pure Python, thread-safe, zero external dependency.
"""

import time
from collections import defaultdict
from threading import Lock
from typing import Dict, List
from fastapi import HTTPException, Request


class SlidingWindowRateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, List[float]] = defaultdict(list)
        self.lock = Lock()

    def is_allowed(self, client_id: str) -> bool:
        now = time.time()
        cutoff = now - self.window_seconds
        with self.lock:
            timestamps = self.requests[client_id]
            # Prune timestamps older than window
            self.requests[client_id] = [t for t in timestamps if t > cutoff]
            if len(self.requests[client_id]) >= self.max_requests:
                return False
            self.requests[client_id].append(now)
            return True

    def check_rate_limit(self, client_id: str):
        if not self.is_allowed(client_id):
            raise HTTPException(
                status_code=429,
                detail=f"Too many requests. Rate limit of {self.max_requests} requests per {self.window_seconds}s exceeded."
            )


# Global rate limiter instances:
# Login: max 15 attempts per minute per IP
login_rate_limiter = SlidingWindowRateLimiter(max_requests=15, window_seconds=60)

# AI inference: max 30 requests per minute per user
ai_rate_limiter = SlidingWindowRateLimiter(max_requests=30, window_seconds=60)


def get_client_ip(request: Request) -> str:
    """Safely extracts client IP address."""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "127.0.0.1"

