from typing import Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def get_authors(
    location_id: str,
    headers: Dict[str, str],
    limit: int = 5,
    offset: int = 0
) -> Dict[str, Any]:
    """
    Get all authors for a given location ID.

    Args:
        location_id: The ID of the location
        headers: Dictionary containing Authorization and Version headers
        limit: Number of authors to show in the listing (default: 5)
        offset: Number of authors to skip in listing (default: 0)

    Returns:
        Dictionary containing the authors data

    Raises:
        Exception: If the API request fails or if required headers are missing
    """
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    if not headers.get("Version"):
        headers["Version"] = API_VERSION

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

    url = f"{API_BASE_URL}/blogs/authors"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=request_headers, params=params)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {e}")
        raise
    except Exception as e:
        logging.error(f"Error fetching authors: {e}")
        raise