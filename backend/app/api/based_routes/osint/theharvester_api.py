"""
OSINT endpoint using theHarvester submodule (tools/theHarvester)

Main Use Case: Business Email Discovery for Skip Tracing
-------------------------------------------------------
This endpoint is optimized for discovering business-related email addresses via OSINT. It leverages theHarvester's powerful email enumeration capabilities to help you find, validate, and enrich contact information for skip tracing, lead generation, and due diligence workflows.

It also supports subdomain, IP, and URL discovery, but email is the primary focus.

How it works:
- Accepts a domain or IP and queries multiple public sources for associated business emails.
- Returns all discovered emails in a structured JSON response, along with other OSINT data.

Requirements:
- Python 3.11+
- theHarvester installed as a submodule in backend/app/osint/tools/theHarvester
- Optionally configure api-keys.yaml for advanced modules

Security: This endpoint is for demonstration and should be protected in production.
"""

import subprocess
import sys
from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field

from app.api.utils.credits import call_function_with_credits
from app.api.utils.credits_estimation import estimate_theharvester_credits

router = APIRouter(prefix="/osint/theharvester", tags=["theHarvester OSINT"])


class HarvesterRequest(BaseModel):
    target: str = Field(..., description="Domain, Email or IP to gather OSINT for")
    modules: list[str] | None = Field(
        None,
        description="list of passive/active modules to use (e.g., ['bing', 'crtsh', 'shodan', 'dnsbrute', 'screenshots'])",
    )
    api_keys: dict[str, str] | None = Field(
        None,
        description="Optional API keys for modules that require them (module_name: key)",
    )
    result_limit: int | None = Field(
        100, description="Maximum number of results per module"
    )
    screenshots: bool | None = Field(
        False, description="Take screenshots of discovered subdomains"
    )
    extra_options: dict[str, Any] | None = Field(
        None, description="Any extra options for advanced usage"
    )


class HarvesterResponse(BaseModel):
    emails: list[str]  # Main use case: discovered business emails
    names: list[str]
    ips: list[str]
    subdomains: list[str]
    urls: list[str]
    screenshots: list[str] | None = None  # URLs or base64 images
    raw_module_results: dict[str, Any] | None = None  # For advanced users
    credits_used: int | None = None  # Credits used for this request


@router.post("/search", response_model=HarvesterResponse)
async def theharvester_search(
    req: HarvesterRequest,
    request: Request,
    current_user=Depends(None),
    db=Depends(None),
):
    # --- Phase 1: Estimate credits and check before running theHarvester ---
    estimated_credits = estimate_theharvester_credits(req)

    # Pre-check: use a dummy function to just check credits
    async def dummy_logic(_request, _current_user):
        return {"detail": "Credit check passed. Proceeding with theHarvester."}

    await call_function_with_credits(
        dummy_logic,
        request,
        credit_type="skiptrace",
        db=db,
        current_user=current_user,
        credit_amount=estimated_credits,
    )
    # --- Phase 2: Run main logic and charge actual credits ---
    harvester_path = "../../osint/tools/theHarvester/theHarvester.py"
    modules_arg = ",".join(req.modules) if req.modules else "all"
    cmd = [
        sys.executable,
        harvester_path,
        "-d",
        req.target,
        "-b",
        modules_arg,
        "-l",
        str(req.result_limit),
    ]
    if req.screenshots:
        cmd.append("--screenshots")
    # TODO: Pass API keys and extra_options if supported by CLI
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
        # TODO: Parse proc.stdout/proc.stderr to extract structured data.
        # For now, return dummy structured data for demonstration:
        dummy_emails = [f"admin@{req.target}", f"info@{req.target}"]
        dummy_response = HarvesterResponse(
            emails=dummy_emails,  # Example: multiple discovered emails
            names=["Jane Doe"],
            ips=["93.184.216.34"],
            subdomains=[f"mail.{req.target}"],
            urls=[f"https://{req.target}"],
            screenshots=["data:image/png;base64,..."] if req.screenshots else None,
            raw_module_results={"stdout": proc.stdout, "stderr": proc.stderr},
        )
        # Calculate average of emails and names array lengths for fair credit usage
        email_count = len(dummy_response.emails) if dummy_response.emails else 0
        name_count = len(dummy_response.names) if dummy_response.names else 0
        if email_count and name_count:
            num_items = max(round((email_count + name_count) / 2), 1)
        else:
            num_items = max(email_count, name_count, 1)
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"theHarvester failed: {e.stderr}")

    async def endpoint_logic(_request, _current_user):
        return dummy_response.dict() | {"credits_used": num_items}

    return await call_function_with_credits(
        endpoint_logic,
        request,
        credit_type="skiptrace",
        db=db,
        current_user=current_user,
        credit_amount=num_items,
    )
