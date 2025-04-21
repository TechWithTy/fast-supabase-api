from typing import Dict, Any, Optional
import httpx

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def list_products(
    headers: Dict[str, str],
    location_id: str,
    limit: Optional[int] = 0,
    offset: Optional[int] = 0,
    search: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieve a paginated list of products.

    Args:
        headers: Dictionary containing Authorization and Version headers.
        location_id: The ID of the sub-account location.
        limit: The maximum number of items per page (default: 0).
        offset: The starting index of the page (default: 0).
        search: The name of the product to search for (optional).

    Returns:
        A dictionary containing the list of products and total count.

    Raises:
        Exception: If the API request fails or if required headers are missing.
    """
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise Exception("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    if not headers.get("Version"):
        headers["Version"] = API_VERSION

    url = f"{API_BASE_URL}/products/"

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

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=request_headers, params=params)
        response.raise_for_status()
        return response.json()