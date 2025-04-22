import asyncio
import os
import sys
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

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
async def zehef_email_lookup(req: ZehefEmailRequest):
    """
    Endpoint to lookup public OSINT information on an email address using Zehef.
    Zehef features include:
        - Checking if the email is in a paste (Pastebin)
        - Finding leaks with HudsonRock
        - Checking social media accounts (Instagram, Spotify, Deezer, Adobe, X, etc.)
        - Generating email combinations
    Zehef is licensed under GPL v3 and requires Python 3.10+.
    """
    try:
        import contextlib
        import io

        output = io.StringIO()
        sys.argv = ["zehef", req.email]
        with contextlib.redirect_stdout(output):
            await zehef_parser()
        result = output.getvalue()
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
