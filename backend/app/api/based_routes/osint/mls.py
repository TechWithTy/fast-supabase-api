import logging
import sys
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request

# Add HomeHarvest to path and import scrape_property
from homeharvest import scrape_property
from pydantic import BaseModel

from app.api.utils.credits import call_function_with_credits
from app.api.utils.credits_estimation import estimate_mls_credits

router = APIRouter(prefix="/mls", tags=["MLS Property Info"])


class MLSPropertyRequest(BaseModel):
    location: str
    listing_type: str = "for_sale"
    return_type: str = "pandas"
    property_type: list[str] = None
    radius: float = None
    mls_only: bool = False
    past_days: int = None
    proxy: str = None
    date_from: str = None
    date_to: str = None
    foreclosure: bool = None
    extra_property_data: bool = True
    exclude_pending: bool = False
    limit: int = 10000


@router.post("/property-info", response_model=Any)
async def mls_property_info_endpoint(
    req: MLSPropertyRequest,
    request: Request,
    current_user=Depends(None),
    db=Depends(None),
):
    # --- Phase 1: Estimate credits and check before running scrape ---
    estimated_credits = estimate_mls_credits(req)
    # Pre-check: use a dummy function to just check credits
    async def dummy_logic(_request, _current_user):
        return {"detail": "Credit check passed. Proceeding with MLS scrape."}
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
        results = scrape_property(
            location=req.location,
            listing_type=req.listing_type,
            return_type=req.return_type,
            property_type=req.property_type,
            radius=req.radius,
            mls_only=req.mls_only,
            past_days=req.past_days,
            proxy=req.proxy,
            date_from=req.date_from,
            date_to=req.date_to,
            foreclosure=req.foreclosure,
            extra_property_data=req.extra_property_data,
            exclude_pending=req.exclude_pending,
            limit=req.limit,
        )
        # If pandas DataFrame, convert to dict
        if hasattr(results, "to_dict"):
            results_dict = results.to_dict(orient="records")
            num_items = max(len(results_dict), 1)
            final_results = results_dict
        else:
            num_items = 1
            final_results = results
    except Exception as e:
        logging.error(f"Error in /mls/property-info: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    async def endpoint_logic(_request, _current_user):
        return {"results": final_results, "credits_used": num_items}
    return await call_function_with_credits(
        endpoint_logic,
        request,
        credit_type="skiptrace",
        db=db,
        current_user=current_user,
        credit_amount=num_items,
    )
