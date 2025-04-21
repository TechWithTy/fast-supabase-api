from typing import Dict, Any, Optional
import httpx

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def fetch_funnel_page_count(
    headers: Dict[str, str],
    funnel_id: str,
    location_id: str,
    name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Fetch count of funnel pages.

    Args:
        headers: Dictionary containing Authorization and Version headers
        funnel_id: The ID of the funnel
        location_id: The ID of the location
        name: Optional name parameter for filtering

    Returns:
        Dictionary containing the count of funnel pages

    Raises:
        httpx.HTTPStatusError: If the API request fails
        ValueError: If required headers are missing
    """
    url = f"{API_BASE_URL}/funnels/page/count"

    if "Authorization" not in headers or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header")

    if "Version" not in headers:
        headers["Version"] = API_VERSION

    headers["Accept"] = "application/json"

    params = {
        "funnelId": funnel_id,
        "locationId": location_id
    }

    if name:
        params["name"] = name

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()