from typing import Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def delete_social_media_post(
    location_id: str,
    post_id: str,
    headers: Dict[str, str]
) -> Dict[str, Any]:
    """
    Delete a social media post.

    Args:
        location_id: The ID of the location
        post_id: The ID of the post to delete
        headers: Dictionary containing Authorization and Version headers

    Returns:
        Dictionary containing the API response

    Raises:
        Exception: If the API request fails or if required headers are missing
    """
    url = f"{API_BASE_URL}/social-media-posting/{location_id}/posts/{post_id}"

    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers.get("Version", API_VERSION),
        "Accept": "application/json"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(url, headers=request_headers)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {e}")
        raise
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise