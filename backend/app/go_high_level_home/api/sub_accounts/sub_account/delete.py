from typing import Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def delete_sub_account(
    location_id: str,
    headers: Dict[str, str],
    delete_twilio_account: bool = False
) -> Dict[str, Any]:
    """
    Delete a Sub-Account (Formerly Location) from the Agency.

    Args:
        location_id: The ID of the location to delete
        headers: Dictionary containing Authorization and Version headers
        delete_twilio_account: Boolean to indicate whether to delete Twilio Account or not

    Returns:
        Dict containing the API response

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

    params = {
        "deleteTwilioAccount": str(delete_twilio_account).lower()
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(url, headers=request_headers, params=params)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {e}")
        raise
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise