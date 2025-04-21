from typing import Dict, Any
import httpx

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def edit_post(headers: Dict[str, str], location_id: str, post_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    url = f"{API_BASE_URL}/social-media-posting/{location_id}/posts/{post_id}"
    
    request_headers = {
        "Accept": "application/json",
        "Authorization": headers.get("Authorization", ""),
        "Content-Type": "application/json",
        "Version": API_VERSION
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.put(url, headers=request_headers, json=payload)
        response.raise_for_status()
        return response.json()