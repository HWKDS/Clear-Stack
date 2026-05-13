import time
from typing import Dict, Tuple

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse

from apps.ai_service.core.config import settings
from apps.ai_service.core.response import error_response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple in-memory token-bucket rate limiter.

    - Keys are `x-api-key` if provided, otherwise client IP.
    - Tokens refill at `rate_limit_per_minute / 60` tokens/sec.
    - Uses in-process state (suitable for single-process dev/test).
    """

    def __init__(self, app) -> None:
        super().__init__(app)
        # mapping: key -> (tokens: float, last_timestamp: float)
        self._buckets: Dict[str, Tuple[float, float]] = {}

    async def dispatch(self, request: Request, call_next):
        limit = int(settings.rate_limit_per_minute or 0)
        if limit <= 0:
            return await call_next(request)

        key = request.headers.get("x-api-key") or (request.client.host if request.client else "anon")
        capacity = float(limit)
        refill_per_sec = capacity / 60.0

        now = time.monotonic()
        tokens, last = self._buckets.get(key, (capacity, now))

        # Refill
        tokens = min(capacity, tokens + (now - last) * refill_per_sec)

        if tokens < 1.0:
            return JSONResponse(status_code=429, content=error_response("Too many requests", "rate_limited"))

        tokens -= 1.0
        self._buckets[key] = (tokens, now)

        return await call_next(request)
