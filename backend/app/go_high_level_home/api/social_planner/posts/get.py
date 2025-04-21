from typing import Dict, Any
import httpx

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def get_post(headers: Dict[str, str], location_id: str, post_id: str) -> Dict[str, Any]:
    """
    Get a social media post from Go High Level API.

    Args:
        headers: Dictionary containing Authorization and Version headers
        location_id: The ID of the location
        post_id: The ID of the post to retrieve

    Returns:
        Dictionary containing the post data

    Raises:
        httpx.HTTPStatusError: If the API request fails
        ValueError: If required headers are missing
    """
    url = f"{API_BASE_URL}/social-media-posting/{location_id}/posts/{post_id}"

    if "Authorization" not in headers or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header")

    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers.get("Version", API_VERSION),
        "Accept": "application/json"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=request_headers)
        response.raise_for_status()
        return response.json()