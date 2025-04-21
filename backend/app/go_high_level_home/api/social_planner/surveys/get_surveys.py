from typing import Dict, Any, Optional
import httpx

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def get_surveys(
    headers: Dict[str, str],
    location_id: str,
    limit: Optional[int] = 10,
    skip: Optional[int] = 0,
    survey_type: Optional[str] = None
) -> Dict[str, Any]:
    url = f"{API_BASE_URL}/surveys/"
    
    if "Authorization" not in headers or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header")

    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers.get("Version", API_VERSION),
        "Accept": "application/json"
    }
    
    params = {
        "locationId": location_id,
        "limit": limit,
        "skip": skip
    }
    
    if survey_type:
        params["type"] = survey_type

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=request_headers, params=params)
        response.raise_for_status()
        return response.json()