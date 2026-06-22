import time
from fastapi import Request, HTTPException

_buckets: dict[str, list[float]] = {}
WINDOW = 60
MAX_REQUESTS = 30


async def rate_limit(request: Request, call_next):
    client = request.client.host if request.client else "unknown"
    now = time.monotonic()
    window = _buckets.setdefault(client, [])
    _buckets[client] = [t for t in window if now - t < WINDOW]
    if len(_buckets[client]) >= MAX_REQUESTS:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    _buckets[client].append(now)
    return await call_next(request)
