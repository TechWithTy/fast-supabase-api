from typing import Dict, Any, Optional
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def fetch_redirect_list(
    headers: Dict[str, str],
    location_id: str,
    limit: int = 20,
    offset: int = 0,
    search: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieves a list of all URL redirects based on the given query parameters.

    Args:
        headers: Dictionary containing Authorization and Version headers
        location_id: The location ID
        limit: Maximum number of results to return (default: 20)
        offset: Number of results to skip (default: 0)
        search: Optional search string

    Returns:
        Dictionary containing the count of redirects and an array of redirect data

    Raises:
        Exception: If the API request fails or if required headers are missing
    """
    url = f"{API_BASE_URL}/funnels/lookup/redirect/list"

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
        "limit": limit,
        "offset": offset
    }

    if search:
        params["search"] = search

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=request_headers, params=params)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"API request failed: {str(e)}")
        raise Exception(f"API request failed: {str(e)}")