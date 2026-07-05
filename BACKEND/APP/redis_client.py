import os

import redis.asyncio as redis

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

_client = None


def get_redis():
    """
    Lazily-created, process-wide async Redis client. redis-py's async
    client is safe to share across coroutines/requests within one process.
    """
    global _client
    if _client is None:
        _client = redis.from_url(REDIS_URL, decode_responses=True)
    return _client
