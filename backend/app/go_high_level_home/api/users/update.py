import httpx
from typing import Dict, Any

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def update_user(user_id: str, user_data: Dict[str, Any], headers: Dict[str, str]) -> Dict[str, Any]:
    url = f"{API_BASE_URL}/users/{user_id}"
    
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")
    
    request_headers = {
        "Accept": "application/json",
        "Authorization": headers["Authorization"],
        "Content-Type": "application/json",
        "Version": headers.get("Version", API_VERSION)
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.put(url, headers=request_headers, json=user_data)
        response.raise_for_status()
        return response.json()