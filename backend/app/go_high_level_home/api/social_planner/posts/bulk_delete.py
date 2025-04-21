from typing import List, Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def bulk_delete_social_planner_posts(
    headers: Dict[str, str],
    location_id: str,
    post_ids: List[str]
) -> Dict[str, Any]:
    """
    Bulk delete social planner posts.

    Args:
        headers: Dictionary containing Authorization and Version headers
        location_id: The ID of the location
        post_ids: List of post IDs to delete (max 50)

    Returns:
        Dictionary containing the API response

    Raises:
        Exception: If the API request fails or if required headers are missing
    """
    url = f"{API_BASE_URL}/social-media-posting/{location_id}/posts/bulk-delete"

    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise Exception("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    if not headers.get("Version"):
        headers["Version"] = API_VERSION

    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers["Version"],
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    data = {"postIds": post_ids}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=request_headers, json=data)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {e}")
        raise Exception(f"Failed to bulk delete social planner posts: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise Exception(f"An error occurred while bulk deleting social planner posts: {e}")