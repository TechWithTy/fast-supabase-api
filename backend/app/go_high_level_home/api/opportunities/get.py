from typing import Dict, Any
import httpx

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def get_opportunity(opportunity_id: str, headers: Dict[str, str]) -> Dict[str, Any]:
    """
    Get an opportunity by its ID.

    Args:
        opportunity_id (str): The ID of the opportunity to retrieve.
        headers (Dict[str, str]): The headers containing the authorization token.

    Returns:
        Dict[str, Any]: The opportunity data.

    Raises:
        httpx.HTTPStatusError: If the API request fails.
        ValueError: If the Authorization header is missing or invalid.
    """
    url = f"{API_BASE_URL}/opportunities/{opportunity_id}"
    
    if "Authorization" not in headers or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header")
    
    request_headers = {
        "Accept": "application/json",
        "Authorization": headers["Authorization"],
        "Version": headers.get("Version", API_VERSION)
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=request_headers)
        response.raise_for_status()
        return response.json()