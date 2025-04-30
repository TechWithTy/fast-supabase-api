import asyncio
import os
import sys
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from app.api.utils.credits import call_function_with_credits
from app.api.utils.credits_estimation import estimate_zehef_credits

# Ensure Zehef is on sys.path for imports (absolute path for reliability)
zehef_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../osint/Zehef")
)
if zehef_path not in sys.path:
    sys.path.append(zehef_path)

from app.osint.Zehef.lib.cli import parser as zehef_parser  # noqa: E402

router = APIRouter(prefix="/osint/zehef", tags=["Zehef OSINT Email"])


class ZehefEmailRequest(BaseModel):
    email: str


@router.post("/email", response_model=dict[str, Any])
async def zehef_email_lookup(
    req: ZehefEmailRequest,
    request: Request,
    current_user=Depends(None),
    db=Depends(None),
):
    """
    Endpoint to lookup public OSINT information on an email address using Zehef.
    Zehef features include:
        - Checking if the email is in a paste (Pastebin)
        - Finding leaks with HudsonRock
        - Checking social media accounts (Instagram, Spotify, Deezer, Adobe, X, etc.)
        - Generating email combinations
    Zehef is licensed under GPL v3 and requires Python 3.10+.
    """

    # --- Phase 1: Estimate credits and check before running Zehef ---
    estimated_credits = estimate_zehef_credits(req)
    # Pre-check: use a dummy function to just check credits
    async def dummy_logic(_request, _current_user):
        return {"detail": "Credit check passed. Proceeding with Zehef."}
    await call_function_with_credits(
        dummy_logic,
        request,
        credit_type="skiptrace",
        db=db,
        current_user=current_user,
        credit_amount=estimated_credits,
    )
    # --- Phase 2: Run main logic and charge actual credits ---
    async def endpoint_logic(_request, _current_user):
        try:
            import contextlib
            import io

            output = io.StringIO()
            sys.argv = ["zehef", req.email]
            with contextlib.redirect_stdout(output):
                await zehef_parser()
            result = output.getvalue()
            # Attempt to parse result for emails/names arrays for fair credit usage
            import re
            emails = re.findall(r"[\w\.-]+@[\w\.-]+", result)
            names = re.findall(r"Name: ([^\n]+)", result)
            email_count = len(emails)
            name_count = len(names)
            if email_count and name_count:
                num_items = max(round((email_count + name_count) / 2), 1)
            else:
                num_items = max(email_count, name_count, 1)
            return {"result": result, "emails": emails, "names": names, "credits_used": num_items}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # Run once to get credits, default to 1 if parsing fails
    try:
        resp = await endpoint_logic(request, current_user)
        num_items = resp.get("credits_used", 1)
    except Exception:
        num_items = 1

    async def endpoint_logic_wrapper(_request, _current_user):
        # Re-run to get the actual response (ensures idempotency)
        return await endpoint_logic(_request, _current_user)

    return await call_function_with_credits(
        endpoint_logic_wrapper,
        request,
        credit_type="skiptrace",
        db=db,
        current_user=current_user,
        credit_amount=num_items,
    )
