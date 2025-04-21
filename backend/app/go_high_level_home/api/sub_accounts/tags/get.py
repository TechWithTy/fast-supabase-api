from typing import Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def get_tags(location_id: str, headers: Dict[str, str]) -> Dict[str, Any]:
    """
    Get Sub-Account (Formerly Location) Tags from Go High Level API.

    Args:
        location_id: The ID of the location
        headers: Dictionary containing request headers

    Returns:
        Dictionary containing the tags data

    Raises:
        Exception: If the API request fails or if required headers are missing
    """
    url = f"{API_BASE_URL}/locations/{location_id}/tags"

    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise Exception("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers.get("Version", API_VERSION),
        "Accept": "application/json"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=request_headers)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {e}")
        raise Exception(f"API request failed with status {e.response.status_code}")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise