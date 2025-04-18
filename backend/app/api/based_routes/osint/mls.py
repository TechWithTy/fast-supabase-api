import logging
import sys
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Add HomeHarvest to path and import scrape_property
sys.path.append("../../osint/HomeHarvest/homeharvest")
from homeharvest import scrape_property

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
def mls_property_info_endpoint(req: MLSPropertyRequest):
    try:
        result = scrape_property(
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
            limit=req.limit
        )
        # If pandas DataFrame, convert to dict
        if hasattr(result, 'to_dict'):
            return result.to_dict(orient="records")
        return result
    except Exception as e:
        logging.error(f"Error in /mls/property-info: {e}")
        raise HTTPException(status_code=500, detail=str(e))
