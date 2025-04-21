from typing import Dict, Any
import httpx

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def get_social_media_accounts(headers: Dict[str, str], location_id: str) -> Dict[str, Any]:
    url = f"{API_BASE_URL}/social-media-posting/{location_id}/accounts"
    
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header")
    
    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers.get("Version", API_VERSION),
        "Accept": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=request_headers)
        response.raise_for_status()
        return response.json()