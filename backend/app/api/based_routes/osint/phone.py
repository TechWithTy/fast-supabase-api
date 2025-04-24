import logging
import sys
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from app.api.utils.credits import call_function_with_credits

# Add Phunter path and import phunter_service
sys.path.append("../../osint/Phunter")
from app.osint.Phunter.phunter_service import phunter_service

router = APIRouter(prefix="/osint", tags=["OSINT Phone"])


class PhoneOSINTRequest(BaseModel):
    phone_numbers: list[str]


@router.post("/phone", response_model=Any)
async def phone_osint_endpoint(req: PhoneOSINTRequest, request: Request, current_user=Depends(None), db=Depends(None)):
    async def endpoint_logic(request, current_user):
        try:
            # Call actual Phunter async service
            result = await phunter_service(req.phone_numbers)
            return result
        except Exception as e:
            logging.error(f"Error in /osint/phone: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    return await call_function_with_credits(endpoint_logic, request, current_user, db, credit_cost=5)
