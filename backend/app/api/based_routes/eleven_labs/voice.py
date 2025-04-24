"""
API routes for ElevenLabs Voice Cloning using shared implementation.
"""
import os

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, Depends, Request
from pydantic import BaseModel
from app.api.utils.credits import call_function_with_credits

from app.eleven_labs_home.api.voices.create_voice_clone import (
    create_voice_clone,
)

router = APIRouter(prefix="/elevenlabs", tags=["ElevenLabs Voice Cloning"])

class VoiceCloneResponse(BaseModel):
    voice_id: str
    details: dict

@router.post("/clone-voice", response_model=VoiceCloneResponse)
async def clone_voice(
    name: str = Form(...),
    description: str | None = Form(None),  # noqa: ARG001
    files: list[UploadFile] = File(...),
    request: Request = None,
    current_user=Depends(None),
    db=Depends(None)
):
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="Missing ElevenLabs API Key")
    files_payload = [(file.filename, await file.read()) for file in files]
    async def endpoint_logic(request, current_user):
        try:
            response = create_voice_clone(api_key, name, files_payload)
            return VoiceCloneResponse(voice_id=response.get("voice_id", ""), details=response)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"ElevenLabs API error: {e}")
    return await call_function_with_credits(endpoint_logic, request, current_user, db, credit_cost=5)
