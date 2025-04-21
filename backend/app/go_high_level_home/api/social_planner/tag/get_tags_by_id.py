from typing import Dict, Any, List
import httpx

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def get_tags_by_ids(headers: Dict[str, str], location_id: str, tag_ids: List[str]) -> Dict[str, Any]:
    """
    Get tags by ids.

    Args:
        headers: Dictionary containing Authorization and Version headers.
        location_id: The ID of the location.
        tag_ids: List of tag IDs to fetch.

    Returns:
        A dictionary containing the API response.

    Raises:
        httpx.HTTPStatusError: If the API request fails.
        ValueError: If the required headers are missing.
    """
    if "Authorization" not in headers or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header")

    url = f"{API_BASE_URL}/social-media-posting/{location_id}/tags/details"

    request_headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Version": headers.get("Version", API_VERSION),
        "Authorization": headers["Authorization"]
    }

    data = {"tagIds": tag_ids}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=request_headers, json=data)
        response.raise_for_status()
        return response.json()