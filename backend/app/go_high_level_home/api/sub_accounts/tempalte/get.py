from typing import Dict, Any, Optional
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def get_templates(
    location_id: str,
    headers: Dict[str, str],
    origin_id: str,
    deleted: bool = False,
    limit: int = 25,
    skip: int = 0,
    template_type: Optional[str] = None
) -> Dict[str, Any]:
    url = f"{API_BASE_URL}/locations/{location_id}/templates"

    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers.get("Version", API_VERSION),
        "Accept": "application/json"
    }

    params = {
        "originId": origin_id,
        "deleted": str(deleted).lower(),
        "limit": str(limit),
        "skip": str(skip)
    }

    if template_type:
        params["type"] = template_type

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=request_headers, params=params)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {e}")
        raise
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise