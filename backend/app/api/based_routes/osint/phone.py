import logging
import sys
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Add Phunter path and import phunter_service
sys.path.append("../../osint/Phunter")
from backend.app.osint.Phunter.phunter_service import phunter_service

router = APIRouter(prefix="/osint", tags=["OSINT Phone"])

class PhoneOSINTRequest(BaseModel):
    phone_numbers: list[str]

@router.post("/phone", response_model=Any)
async def phone_osint_endpoint(req: PhoneOSINTRequest):
    try:
        # Call actual Phunter async service
        result = await phunter_service(req.phone_numbers)
        return result
    except Exception as e:
        logging.error(f"Error in /osint/phone: {e}")
        raise HTTPException(status_code=500, detail=str(e))
