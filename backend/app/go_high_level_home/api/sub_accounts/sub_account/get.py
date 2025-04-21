from typing import Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def get_sub_account(location_id: str, headers: Dict[str, str]) -> Dict[str, Any]:
    """
    Get details of a Sub-Account (Formerly Location) by passing the sub-account id.

    Args:
        location_id: The ID of the sub-account/location
        headers: Dictionary containing Authorization and Version headers

    Returns:
        Dictionary containing the sub-account details

    Raises:
        Exception: If the API request fails or if required headers are missing
    """
    url = f"{API_BASE_URL}/locations/{location_id}"

    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    if not headers.get("Version"):
        headers["Version"] = API_VERSION

    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers["Version"],
        "Accept": "application/json"
    }

    logging.info(f"Making request to get sub-account details for location: {location_id}")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=request_headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logging.error(f"HTTP error occurred: {e}")
            raise
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            raise