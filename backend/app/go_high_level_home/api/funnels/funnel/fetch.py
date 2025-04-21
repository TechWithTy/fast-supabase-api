from typing import Dict, Any, Optional
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def fetch_funnels(
    headers: Dict[str, str],
    location_id: str,
    category: Optional[str] = None,
    limit: Optional[int] = None,
    name: Optional[str] = None,
    offset: Optional[int] = None,
    parent_id: Optional[str] = None,
    funnel_type: Optional[str] = None
) -> Dict[str, Any]:
    """
    Fetch a list of funnels based on the given query parameters.

    Args:
        headers: Dictionary containing Authorization and Version headers
        location_id: The ID of the location
        category: Optional category filter
        limit: Optional limit for the number of results
        name: Optional name filter
        offset: Optional offset for pagination
        parent_id: Optional parent ID filter
        funnel_type: Optional funnel type filter

    Returns:
        A dictionary containing the list of funnels and metadata

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
        "locationId": location_id,
        "category": category,
        "limit": limit,
        "name": name,
        "offset": offset,
        "parentId": parent_id,
        "type": funnel_type
    }

    params = {k: v for k, v in params.items() if v is not None}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{API_BASE_URL}/funnels/funnel/list",
                headers=request_headers,
                params=params
            )
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {e}")
        raise Exception(f"Failed to fetch funnels: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise Exception(f"An error occurred while fetching funnels: {e}")