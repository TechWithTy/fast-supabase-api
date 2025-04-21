import httpx
from typing import Dict, Any

async def create_invoice_estimate(headers: Dict[str, str], payload: Dict[str, Any]) -> Dict[str, Any]:
    url = "https://services.leadconnectorhq.com/invoices/estimate"
    
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")
    
    request_headers = {
        "Accept": "application/json",
        "Authorization": headers["Authorization"],
        "Content-Type": "application/json",
        "Version": headers.get("Version", "2021-07-28")
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=request_headers, json=payload)
        response.raise_for_status()
        return response.json()