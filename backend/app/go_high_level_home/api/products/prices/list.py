from typing import Dict, Any, Optional
import httpx

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def list_product_prices(
    product_id: str,
    location_id: str,
    headers: Dict[str, str],
    ids: Optional[str] = None,
    limit: Optional[int] = 0,
    offset: Optional[int] = 0
) -> Dict[str, Any]:
    """
    List Prices for a Product

    Args:
        product_id: ID of the product
        location_id: The unique identifier for the location
        headers: Dictionary containing Authorization and Version headers
        ids: Comma-separated price IDs to filter the response
        limit: The maximum number of items per page (default: 0)
        offset: The starting index of the page (default: 0)

    Returns:
        Dictionary containing the list of prices and total count

    Raises:
        httpx.HTTPStatusError: If the API request fails
        Exception: If required headers are missing
    """
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise Exception("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    if not headers.get("Version"):
        headers["Version"] = API_VERSION

    url = f"{API_BASE_URL}/products/{product_id}/price"

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

    if ids:
        params["ids"] = ids

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=request_headers, params=params)
        response.raise_for_status()
        return response.json()