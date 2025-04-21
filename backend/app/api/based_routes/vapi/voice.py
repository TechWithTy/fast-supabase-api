from typing import Any

from backend.app.vapi_home.api.tools.voice.sync_customer_voice import (
    sync_customer_voice_with_vapi,
)
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/vapi/voice", tags=["VAPI Voice Management"])


class VoiceIdUploadRequest(BaseModel):
    voice_id: str
    label: str
    customer_id: str
    meta: dict[str, Any] = {}


@router.post("/upload-elevenlabs-voice")
async def upload_elevenlabs_voice(req: VoiceIdUploadRequest):
    try:
        sync_customer_voice_with_vapi(req.customer_id, req.voice_id)
        return {"status": "success", "voice_id": req.voice_id, "label": req.label}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
