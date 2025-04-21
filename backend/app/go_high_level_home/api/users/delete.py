from typing import Dict, Any
import httpx

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def delete_user(headers: Dict[str, str], user_id: str) -> Dict[str, Any]:
    url = f"{API_BASE_URL}/users/{user_id}"
    
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")
    
    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers.get("Version", API_VERSION),
        "Accept": "application/json"
    }

    async with httpx.AsyncClient() as client:
        response = await client.delete(url, headers=request_headers)
        response.raise_for_status()
        return response.json()