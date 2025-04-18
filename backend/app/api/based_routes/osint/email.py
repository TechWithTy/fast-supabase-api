import sys
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Ensure the correct path for imports
sys.path.append("../../osint/email2phonenumber")
from backend.app.osint.email2phonenumber.email2phonenumber import start_scrapping

router = APIRouter(prefix="/osint", tags=["OSINT Email"])

class EmailToPhoneRequest(BaseModel):
    email: str
    quiet_mode: bool = False
    # extra is not used by start_scrapping, so removed for clarity

@router.post("/email", response_model=dict[str, Any])
async def email_to_phone_endpoint(req: EmailToPhoneRequest):
    """
    Endpoint to lookup phone number information based on an email address using email2phonenumber's start_scrapping.
    """
    try:
        # start_scrapping returns None and prints to stdout, so capture output
        import contextlib
        import io
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            start_scrapping(req.email, req.quiet_mode)
        result = output.getvalue()
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
