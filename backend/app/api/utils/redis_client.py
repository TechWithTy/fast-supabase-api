import os
import redis.asyncio as redis
from fastapi import Request

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# No on_event or register_redis_events needed; handled via FastAPI lifespan in main.py

async def get_redis_client(request: Request) -> redis.Redis:
    client = getattr(request.app.state, "redis_client", None)
    if client is None:
        raise RuntimeError("Redis client not initialized via lifespan event.")
    return client
