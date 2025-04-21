from typing import Dict, Any, List
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def get_user_by_location(headers: Dict[str, str], location_id: str) -> Dict[str, Any]:
    """
    Get User by Location.

    Args:
        headers (Dict[str, str]): The request headers containing the authorization token.
        location_id (str): The ID of the location.

    Returns:
        Dict[str, Any]: The response containing user information.

    Raises:
        httpx.HTTPStatusError: If the API request fails.
        ValueError: If the required headers are missing.
    """
    url = f"{API_BASE_URL}/users/"
    
    if "Authorization" not in headers or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header")
    
    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers.get("Version", API_VERSION),
        "Accept": "application/json"
    }
    
    params = {
        "locationId": location_id
    }
    
    logging.info(f"Making request to get user for location: {location_id}")
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=request_headers, params=params)
        response.raise_for_status()
        return response.json()