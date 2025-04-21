from typing import Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def update_custom_field(
    location_id: str,
    custom_field_id: str,
    headers: Dict[str, str],
    custom_field_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Update a custom field in Go High Level.

    Args:
        location_id: The ID of the location
        custom_field_id: The ID of the custom field to update
        headers: Dictionary containing Authorization and Version headers
        custom_field_data: Dictionary containing custom field details to update

    Returns:
        Dictionary containing the updated custom field data

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
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    logging.info(f"Updating custom field {custom_field_id} for location {location_id}")

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.put(
                f"{API_BASE_URL}/locations/{location_id}/customFields/{custom_field_id}",
                headers=request_headers,
                json=custom_field_data
            )

        response.raise_for_status()
        return response.json()

    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {e}")
        raise Exception(f"Failed to update custom field: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise Exception(f"An error occurred while updating custom field: {e}")