from typing import Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def get_custom_value(location_id: str, custom_value_id: str, headers: Dict[str, str]) -> Dict[str, Any]:
    """
    Get a custom value from Go High Level API.

    Args:
        location_id: The ID of the location
        custom_value_id: The ID of the custom value
        headers: Dictionary containing Authorization and Version headers

    Returns:
        Dictionary containing the custom value data

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

    url = f"{API_BASE_URL}/locations/{location_id}/customValues/{custom_value_id}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=request_headers)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {e}")
        raise Exception(f"Failed to get custom value: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise Exception(f"An error occurred while getting custom value: {e}")