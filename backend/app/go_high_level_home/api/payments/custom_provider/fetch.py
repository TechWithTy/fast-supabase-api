from typing import Dict, Any
import httpx

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def fetch_custom_provider(headers: Dict[str, str], location_id: str) -> Dict[str, Any]:
    """
    Fetch an existing payment config for a given location.

    Args:
        headers (Dict[str, str]): The headers containing the authorization token.
        location_id (str): The ID of the location.

    Returns:
        Dict[str, Any]: The custom provider configuration.

    Raises:
        httpx.HTTPStatusError: If the API request fails.
        ValueError: If the Authorization header is missing or invalid.
    """
    url = f"{API_BASE_URL}/payments/custom-provider/connect"
    
    if "Authorization" not in headers or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header")

    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": API_VERSION,
        "Accept": "application/json"
    }
    
    params = {
        "locationId": location_id
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=request_headers, params=params)
        response.raise_for_status()
        return response.json()