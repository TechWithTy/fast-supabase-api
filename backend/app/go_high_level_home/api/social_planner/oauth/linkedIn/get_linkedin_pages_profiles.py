from typing import Dict, Any
import httpx

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def get_linkedin_pages_profiles(headers: Dict[str, str], location_id: str, account_id: str) -> Dict[str, Any]:
    url = f"{API_BASE_URL}/social-media-posting/oauth/{location_id}/linkedin/accounts/{account_id}"
    
    if "Authorization" not in headers or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header")
    
    request_headers = {
        "Accept": "application/json",
        "Authorization": headers["Authorization"],
        "Version": headers.get("Version", API_VERSION)
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=request_headers)
        response.raise_for_status()
        return response.json()