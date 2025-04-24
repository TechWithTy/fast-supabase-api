from typing import Any

from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from app.vapi_home.api.tools.voice.sync_customer_voice import (
    sync_customer_voice_with_vapi,
)
from app.api.utils.credits import call_function_with_credits

router = APIRouter(prefix="/vapi/voice", tags=["VAPI Voice Management"])


class VoiceIdUploadRequest(BaseModel):
    voice_id: str
    label: str
    customer_id: str
    meta: dict[str, Any] = {}


@router.post("/upload-elevenlabs-voice")
async def upload_elevenlabs_voice(req: VoiceIdUploadRequest, request: Request, current_user=Depends(None), db=Depends(None)):
    async def endpoint_logic(request, current_user):
        try:
            sync_customer_voice_with_vapi(req.customer_id, req.voice_id)
            return {"status": "success", "voice_id": req.voice_id, "label": req.label}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    return await call_function_with_credits(endpoint_logic, request, current_user, db, credit_cost=0)
