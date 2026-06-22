import json
import uuid
import logging
import redis.asyncio as aioredis
import os

logger = logging.getLogger(__name__)

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

_redis: aioredis.Redis | None = None


def _get_redis() -> aioredis.Redis:
    global _redis
    if _redis is None:
        _redis = aioredis.from_url(REDIS_URL, decode_responses=True)
    return _redis


async def create_reminder(data: dict) -> dict:
    reminder_id = str(uuid.uuid4())
    reminder = {**data, "id": reminder_id, "active": True}
    r = _get_redis()
    await r.set(f"reminder:{reminder_id}", json.dumps(reminder))
    await r.sadd(f"user_reminders:{data['user_id']}", reminder_id)
    logger.info("Created reminder %s for user %s", reminder_id, data["user_id"])
    return reminder


async def get_reminder(reminder_id: str) -> dict | None:
    r = _get_redis()
    raw = await r.get(f"reminder:{reminder_id}")
    return json.loads(raw) if raw else None


async def delete_reminder(reminder_id: str) -> bool:
    r = _get_redis()
    existing = await r.get(f"reminder:{reminder_id}")
    if not existing:
        return False
    data = json.loads(existing)
    await r.delete(f"reminder:{reminder_id}")
    await r.srem(f"user_reminders:{data['user_id']}", reminder_id)
    return True


async def list_reminders(user_id: str) -> list[dict]:
    r = _get_redis()
    ids = await r.smembers(f"user_reminders:{user_id}")
    results = []
    for rid in ids:
        raw = await r.get(f"reminder:{rid}")
        if raw:
            results.append(json.loads(raw))
    return results
