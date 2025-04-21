from typing import Dict, Any, Optional
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def get_blog_posts_by_id(
    headers: Dict[str, str],
    blog_id: str,
    location_id: str,
    limit: int,
    offset: int,
    search_term: Optional[str] = None,
    status: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get blog posts by Blog ID from the Go High Level API.

    Args:
        headers: Dictionary containing Authorization and Version headers
        blog_id: The ID of the blog
        location_id: The ID of the location
        limit: Maximum number of posts to return
        offset: Number of posts to skip
        search_term: Optional search term for posts
        status: Optional status filter (PUBLISHED, SCHEDULED, ARCHIVED, DRAFT)

    Returns:
        Dictionary containing the blog posts data

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
        "blogId": blog_id,
        "locationId": location_id,
        "limit": limit,
        "offset": offset
    }

    if search_term:
        params["searchTerm"] = search_term
    if status:
        params["status"] = status

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                f"{API_BASE_URL}/blogs/posts/all",
                headers=request_headers,
                params=params
            )

        response.raise_for_status()
        return response.json()

    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {e}")
        raise Exception(f"API request failed with status {e.response.status_code}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise