from typing import Dict, Any, Optional
import httpx

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def list_estimate_templates(
    headers: Dict[str, str],
    alt_id: str,
    alt_type: str = "location",
    limit: int = 10,
    offset: int = 0,
    search: Optional[str] = None
) -> Dict[str, Any]:
    url = f"{API_BASE_URL}/invoices/estimate/template"
    
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    request_headers = {
        "Accept": "application/json",
        "Authorization": headers["Authorization"],
        "Version": headers.get("Version", API_VERSION)
    }
    
    params = {
        "altId": alt_id,
        "altType": alt_type,
        "limit": limit,
        "offset": offset
    }
    
    if search:
        params["search"] = search
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=request_headers, params=params)
        response.raise_for_status()
        return response.json()