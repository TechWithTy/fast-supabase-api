from typing import Dict, Any
import httpx

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def get_price_by_id(
    headers: Dict[str, str],
    product_id: str,
    price_id: str,
    location_id: str
) -> Dict[str, Any]:
    """
    Get Price by ID for a Product

    Args:
        headers: Dictionary containing Authorization and Version headers
        product_id: ID of the product
        price_id: ID of the price
        location_id: ID of the location

    Returns:
        Dictionary containing the price details

    Raises:
        httpx.HTTPStatusError: If the API request fails
        Exception: If required headers are missing
    """
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise Exception("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    if not headers.get("Version"):
        headers["Version"] = API_VERSION

    url = f"{API_BASE_URL}/products/{product_id}/price/{price_id}"

    request_headers = {
        "Accept": "application/json",
        "Authorization": headers["Authorization"],
        "Version": headers["Version"]
    }

    params = {
        "locationId": location_id
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=request_headers, params=params)
        response.raise_for_status()
        return response.json()