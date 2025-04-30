# TODO: Updates needed for our Phunter fork:
# 1. Add support for accepting an array (list) of phone numbers as input, not just single numbers or files.
#    - The CLI and Python interface should accept a list and process each number in a loop.
# 2. Output results as a Python list/array (JSON-serializable), not just to a file.
#    - When given multiple numbers, return a list of results (one per input number), not a file path.
#    - When given a single number, return a single result (not a file).
# 3. Ensure all modes (info, amazon, person) work with both single and multiple inputs.
# 4. Remove or make optional the file output argument for API/library use.
# 5. Add tests for bulk input and JSON output for all modes.
# 6. Update documentation to reflect new input/output options for both CLI and Python usage.

import logging
import sys
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field

from app.api.utils.credits import call_function_with_credits
from app.api.utils.credits_estimation import estimate_phone_credits

# Add Phunter path and import phunter_service
sys.path.append("../../osint/Phunter")
from app.osint.Phunter.phunter_service import phunter_service

router = APIRouter(prefix="/osint", tags=["OSINT Phone"])


class PhoneOSINTRequest(BaseModel):
    phone_numbers: list[str] = Field(..., description="Array of phone numbers to query (bulk or single)")
    mode: str = Field("info", description="Type of lookup: 'info', 'amazon', or 'person'")
    output: str | None = Field(None, description="Output file name (optional, for future use)")
    verify: bool | None = Field(False, description="Check version/services (optional)")


@router.post("/phone", response_model=Any)
async def phone_osint_endpoint(
    req: PhoneOSINTRequest,
    request: Request,
    current_user=Depends(None),
    db=Depends(None),
):
    # --- Phase 1: Estimate credits and check before running phone OSINT ---
    estimated_credits = estimate_phone_credits(req)
    # Pre-check: use a dummy function to just check credits
    async def dummy_logic(_request, _current_user):
        return {"detail": "Credit check passed. Proceeding with phone OSINT."}
    await call_function_with_credits(
        dummy_logic,
        request,
        credit_type="skiptrace",
        db=db,
        current_user=current_user,
        credit_amount=estimated_credits,
    )
    # --- Phase 2: Run main logic and charge actual credits ---
    try:
        results = []
        for phone in req.phone_numbers:
            if req.mode == "amazon":
                result = await phunter_service(phone, amazon=True, output=req.output, verify=req.verify)
            elif req.mode == "person":
                result = await phunter_service(phone, person=True, output=req.output, verify=req.verify)
            else:
                result = await phunter_service(phone, output=req.output, verify=req.verify)
            # If pandas DataFrame, convert to dict
            if hasattr(result, "to_dict"):
                results.append(result.to_dict(orient="records"))
            else:
                results.append(result)
        # If only one phone number, return single result for convenience
        final_result = results[0] if len(results) == 1 else results
        # Actual credits: number of phone numbers processed (for fairness, could use number of valid results if needed)
        num_items = max(len(req.phone_numbers), 1)
    except Exception as e:
        logging.error(f"Error in /osint/phone: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    async def endpoint_logic(_request, _current_user):
        return {"results": final_result, "credits_used": num_items}
    return await call_function_with_credits(
        endpoint_logic,
        request,
        credit_type="skiptrace",
        db=db,
        current_user=current_user,
        credit_amount=num_items,
    )
