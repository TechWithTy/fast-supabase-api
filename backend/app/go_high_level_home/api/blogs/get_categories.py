from typing import Dict, Any, Optional
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def get_blog_categories(
    location_id: str,
    headers: Dict[str, str],
    limit: int = 10,
    offset: int = 0
) -> Dict[str, Any]:
    """
    Get all blog categories for a given location ID.

    Args:
        location_id: The ID of the location to fetch categories for
        headers: Dictionary containing Authorization and Version headers
        limit: Number of categories to show in the listing (default: 10)
        offset: Number of categories to skip in listing (default: 0)

    Returns:
        Dictionary containing the blog categories data

    Raises:
        Exception: If the API request fails or if required headers are missing
    """
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise Exception("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    if not headers.get("Version"):
        headers["Version"] = API_VERSION

    url = f"{API_BASE_URL}/blogs/categories"

    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers["Version"],
        "Accept": "application/json"
    }

    params = {
        "locationId": location_id,
        "limit": limit,
        "offset": offset
    }

    logging.info(f"Getting blog categories for location: {location_id}")

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(url, headers=request_headers, params=params)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {e}")
        raise
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise