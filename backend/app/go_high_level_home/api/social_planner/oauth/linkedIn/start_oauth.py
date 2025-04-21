from typing import Dict, Any
import httpx

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def start_linkedin_oauth(
    headers: Dict[str, str],
    location_id: str,
    user_id: str,
    page: str = "integration",
    reconnect: str = "true"
) -> Dict[str, Any]:
    if "Authorization" not in headers or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header")

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

    url = f"{API_BASE_URL}/social-media-posting/oauth/linkedin/start"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=request_headers, params=params)
        response.raise_for_status()
        return response.json()