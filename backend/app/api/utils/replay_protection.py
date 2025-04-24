import time
from app.api.utils.redis_client import redis_client
from fastapi import HTTPException

NONCE_EXPIRY = 300  # seconds

async def check_and_store_nonce(nonce: str) -> bool:
    key = f"nonce:{nonce}"
    exists = await redis_client.get(key)
    if exists:
        raise HTTPException(status_code=409, detail="Replay attack detected (nonce reused)")
    await redis_client.set(key, "1", ex=NONCE_EXPIRY)
    return True
