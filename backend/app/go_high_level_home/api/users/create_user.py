from typing import Dict, Any
import httpx

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def create_user(headers: Dict[str, str]) -> Dict[str, Any]:
    url = f"{API_BASE_URL}/users/"
    
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    request_headers = {
        "Accept": "application/json",
        "Authorization": headers["Authorization"],
        "Content-Type": "application/json",
        "Version": API_VERSION
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=request_headers)
        
        if response.status_code == 201:
            return response.json()
        else:
            raise httpx.HTTPStatusError(f"Error: {response.status_code}", request=response.request, response=response)