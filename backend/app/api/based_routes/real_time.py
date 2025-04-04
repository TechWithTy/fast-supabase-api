from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from ...supabase_home.realtime import SupabaseRealtimeService

app = FastAPI(title="SupabaseRealtimeAPI", description="API to interact with current Realtime functions")

realtime_service = SupabaseRealtimeService()

class SubscriptionRequest(BaseModel):
    channel: str
    event: str = "*"
    auth_token: str | None = None
    is_admin: bool = True

class UnsubscriptionRequest(BaseModel):
    subscription_id: str
    auth_token: str | None = None
    is_admin: bool = True

class BroadcastRequest(BaseModel):
    channel: str
    payload: dict[str, Any]
    event: str = "broadcast"
    auth_token: str | None = None
    is_admin: bool = True

@app.post("/subscribe")
async def subscribe_to_channel(request: SubscriptionRequest):
    try:
        result = realtime_service.subscribe_to_channel(
            channel=request.channel,
            event=request.event,
            auth_token=request.auth_token,
            is_admin=request.is_admin
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/unsubscribe")
async def unsubscribe_from_channel(request: UnsubscriptionRequest):
    try:
        result = realtime_service.unsubscribe_from_channel(
            subscription_id=request.subscription_id,
            auth_token=request.auth_token,
            is_admin=request.is_admin
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/unsubscribe_all")
async def unsubscribe_all(auth_token: str | None = None, is_admin: bool = True):
    try:
        result = realtime_service.unsubscribe_all(auth_token=auth_token, is_admin=is_admin)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/channels")
async def get_channels(auth_token: str | None = None):
    try:
        result = realtime_service.get_channels(auth_token=auth_token)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/broadcast")
async def broadcast_message(request: BroadcastRequest):
    try:
        result = realtime_service.broadcast_message(
            channel=request.channel,
            payload=request.payload,
            event=request.event,
            auth_token=request.auth_token,
            is_admin=request.is_admin
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
