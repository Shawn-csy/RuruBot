import os
import threading
import time
from collections import deque
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

ASK_PATHS = {"/api/ticket", "/api/answers-book"}


def _get_client_ip(request: Request) -> str:
    cf_ip = request.headers.get("cf-connecting-ip")
    if cf_ip:
        return cf_ip.strip()
    xff = request.headers.get("x-forwarded-for")
    if xff:
        return xff.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


class SlidingWindowLimiter:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._buckets: dict[str, deque[float]] = {}
        self._last_gc = time.monotonic()

    def check(self, key: str, limit: int, window_seconds: int) -> tuple[bool, int, int]:
        """Returns (allowed, remaining, retry_after_seconds)."""
        now = time.monotonic()
        cutoff = now - window_seconds

        with self._lock:
            if now - self._last_gc > 300:
                self._gc(now)
                self._last_gc = now

            q = self._buckets.get(key)
            if q is None:
                q = deque()
                self._buckets[key] = q

            while q and q[0] <= cutoff:
                q.popleft()

            if len(q) >= limit:
                retry_after = max(1, int(q[0] + window_seconds - now) + 1)
                return False, 0, retry_after

            q.append(now)
            remaining = max(0, limit - len(q))
            return True, remaining, 0

    def _gc(self, now: float) -> None:
        stale = [k for k, q in self._buckets.items() if not q or now - q[-1] > 3600]
        for k in stale:
            del self._buckets[k]


class ApiRateLimitMiddleware(BaseHTTPMiddleware):
    """Per-IP sliding-window rate limiter for /api/* endpoints only."""

    def __init__(self, app) -> None:
        super().__init__(app)
        self.limiter = SlidingWindowLimiter()
        self.ask_per_min = int(os.getenv("API_ASK_PER_MIN", "10"))
        self.ask_per_hour = int(os.getenv("API_ASK_PER_HOUR", "30"))
        self.read_per_min = int(os.getenv("API_READ_PER_MIN", "30"))

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if not path.startswith("/api/") or request.method == "OPTIONS":
            return await call_next(request)

        ip = _get_client_ip(request)

        if request.method == "POST" and path in ASK_PATHS:
            ok_min, rem_min, retry_min = self.limiter.check(
                f"ask1m:{ip}", self.ask_per_min, 60
            )
            if not ok_min:
                return JSONResponse(
                    status_code=429,
                    content={
                        "detail": f"提問太頻繁了，請於 {retry_min} 秒後再試",
                        "retry_after": retry_min,
                    },
                    headers={
                        "Retry-After": str(retry_min),
                        "X-RateLimit-Limit": str(self.ask_per_min),
                        "X-RateLimit-Remaining": "0",
                    },
                )

            ok_hr, rem_hr, retry_hr = self.limiter.check(
                f"ask1h:{ip}", self.ask_per_hour, 3600
            )
            if not ok_hr:
                mins = max(1, retry_hr // 60)
                return JSONResponse(
                    status_code=429,
                    content={
                        "detail": f"本小時提問次數已達上限，請於 {mins} 分鐘後再試",
                        "retry_after": retry_hr,
                    },
                    headers={
                        "Retry-After": str(retry_hr),
                        "X-RateLimit-Limit": str(self.ask_per_hour),
                        "X-RateLimit-Remaining": "0",
                    },
                )

            response = await call_next(request)
            response.headers["X-RateLimit-Limit"] = str(self.ask_per_min)
            response.headers["X-RateLimit-Remaining"] = str(min(rem_min, rem_hr))
            return response

        ok, rem, retry = self.limiter.check(f"read1m:{ip}", self.read_per_min, 60)
        if not ok:
            return JSONResponse(
                status_code=429,
                content={
                    "detail": f"請求太頻繁了，請於 {retry} 秒後再試",
                    "retry_after": retry,
                },
                headers={
                    "Retry-After": str(retry),
                    "X-RateLimit-Limit": str(self.read_per_min),
                    "X-RateLimit-Remaining": "0",
                },
            )

        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(self.read_per_min)
        response.headers["X-RateLimit-Remaining"] = str(rem)
        return response
