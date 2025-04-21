"""
API routes for ElevenLabs Voice Cloning using shared implementation.
"""
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from typing import Optional
import os
from backend.app.eleven_labs_home.api.voices.create_voice_clone import create_voice_clone

router = APIRouter(prefix="/elevenlabs", tags=["ElevenLabs Voice Cloning"])

class VoiceCloneResponse(BaseModel):
    voice_id: str
    details: dict

@router.post("/clone-voice", response_model=VoiceCloneResponse)
async def clone_voice(
    name: str = Form(...),
    description: Optional[str] = Form(None),
    files: list[UploadFile] = File(...)
):
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="Missing ElevenLabs API Key")
    # Read files into memory for the client
    files_payload = [(file.filename, await file.read()) for file in files]
    try:
        response = create_voice_clone(api_key, name, files_payload)
        # The shared function should return a dict with 'voice_id' and details
        return VoiceCloneResponse(voice_id=response.get("voice_id", ""), details=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ElevenLabs API error: {e}")
