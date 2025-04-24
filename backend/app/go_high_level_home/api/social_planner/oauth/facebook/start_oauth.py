from typing import Dict, Any
import httpx
from fastapi import Request, Depends, HTTPException
from app.api.utils.oauth_scope import require_scope

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def start_facebook_oauth(
    headers: Dict[str, str],
    location_id: str,
    user_id: str,
    page: str = "integration",
    reconnect: str = "true"
) -> Dict[str, Any]:
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers.get("Version", API_VERSION),
        "Accept": "application/json"
    }

    params = {
        "locationId": location_id,
        "userId": user_id,
        "page": page,
        "reconnect": reconnect
    }

    url = f"{API_BASE_URL}/social-media-posting/oauth/facebook/start"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=request_headers, params=params)
        response.raise_for_status()
        return response.json()

# Example FastAPI endpoint enforcing OAuth scope
def facebook_oauth_endpoint(
    request: Request,
    dep=Depends(require_scope("integration:facebook")),
):
    # ...rest of your logic, e.g. call start_facebook_oauth...
    pass