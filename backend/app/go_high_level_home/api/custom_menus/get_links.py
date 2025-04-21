from typing import Dict, Any, Optional
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def get_custom_menu_links(
    headers: Dict[str, str],
    limit: Optional[int] = 20,
    location_id: Optional[str] = None,
    query: Optional[str] = None,
    show_on_company: Optional[bool] = None,
    skip: Optional[int] = 0
) -> Dict[str, Any]:
    """
    Fetches a collection of custom menus based on specified criteria.

    Args:
        headers (Dict[str, str]): Headers containing Authorization and Version.
        limit (int, optional): Maximum number of items to return. Defaults to 20.
        location_id (str, optional): Unique identifier of the location.
        query (str, optional): Search query to filter custom menus by name.
        show_on_company (bool, optional): Filter to show only agency-level menu links.
        skip (int, optional): Number of items to skip for pagination. Defaults to 0.

    Returns:
        Dict[str, Any]: A dictionary containing the custom menu links data.

    Raises:
        Exception: If the API request fails or if required headers are missing.
    """
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise Exception("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    if not headers.get("Version"):
        headers["Version"] = API_VERSION

    url = f"{API_BASE_URL}/custom-menus/"

    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers["Version"],
        "Accept": "application/json"
    }

    params = {
        "limit": limit,
        "locationId": location_id,
        "query": query,
        "showOnCompany": show_on_company,
        "skip": skip
    }

    params = {k: v for k, v in params.items() if v is not None}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=request_headers, params=params)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {e}")
        raise Exception(f"API request failed with status {e.response.status_code}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise