from typing import Dict, Any
import httpx

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def update_estimate_last_visited(headers: Dict[str, str], estimate_id: str) -> Dict[str, Any]:
    url = f"{API_BASE_URL}/invoices/estimate/stats/last-visited-at"
    
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")
    
    request_headers = {
        "Accept": "application/json",
        "Authorization": headers["Authorization"],
        "Content-Type": "application/json",
        "Version": headers.get("Version", API_VERSION)
    }
    
    data = {"estimateId": estimate_id}

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=request_headers, json=data)
        response.raise_for_status()
        return response.json()