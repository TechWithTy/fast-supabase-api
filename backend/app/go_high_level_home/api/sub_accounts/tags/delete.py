from typing import Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def delete_tag(
    location_id: str,
    tag_id: str,
    headers: Dict[str, str]
) -> Dict[str, Any]:
    """
    Delete a tag for a specific location.

    Args:
        location_id: The ID of the location
        tag_id: The ID of the tag to delete
        headers: Dictionary containing Authorization and Version headers

    Returns:
        Dict containing the API response

    Raises:
        ValueError: If required headers are missing
        Exception: If the API request fails
    """
    url = f"{API_BASE_URL}/locations/{location_id}/tags/{tag_id}"

    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers.get("Version", API_VERSION),
        "Accept": "application/json"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(url, headers=request_headers)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {e}")
        raise
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise