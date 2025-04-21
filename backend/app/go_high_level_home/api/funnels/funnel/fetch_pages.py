from typing import Dict, Any, Optional
import httpx

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def fetch_funnel_pages(
    headers: Dict[str, str],
    funnel_id: str,
    location_id: str,
    limit: int,
    offset: int,
    name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Fetch list of funnel pages from the Go High Level API.

    Args:
        headers: Dictionary containing Authorization and Version headers
        funnel_id: The ID of the funnel
        location_id: The ID of the location
        limit: Maximum number of pages to return
        offset: Number of pages to skip
        name: Optional name filter for pages

    Returns:
        Dictionary containing the funnel pages data

    Raises:
        Exception: If the API request fails or if required headers are missing
    """
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise Exception("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    if not headers.get("Version"):
        headers["Version"] = API_VERSION

    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers["Version"],
        "Accept": "application/json"
    }

    params = {
        "funnelId": funnel_id,
        "locationId": location_id,
        "limit": limit,
        "offset": offset
    }

    if name:
        params["name"] = name

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_BASE_URL}/funnels/page",
            headers=request_headers,
            params=params
        )
        response.raise_for_status()
        return response.json()