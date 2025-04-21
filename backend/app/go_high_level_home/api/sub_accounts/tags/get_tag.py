from typing import Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def get_tag(location_id: str, tag_id: str, headers: Dict[str, str]) -> Dict[str, Any]:
    """
    Get tag by id from Go High Level API.

    Args:
        location_id: The ID of the location
        tag_id: The ID of the tag
        headers: Dictionary containing Authorization and Version headers

    Returns:
        Dictionary containing the tag data

    Raises:
        Exception: If the API request fails or if required headers are missing
    """
    url = f"{API_BASE_URL}/locations/{location_id}/tags/{tag_id}"

    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise Exception("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    if not headers.get("Version"):
        headers["Version"] = API_VERSION

    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers["Version"],
        "Accept": "application/json"
    }

    logging.info(f"Making request to get tag: {tag_id} for location: {location_id}")

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(url, headers=request_headers)
        if response.status_code != 200:
            error_detail = response.text
            logging.error(f"API request failed with status {response.status_code}: {error_detail}")
            raise Exception(f"API request failed with status {response.status_code}: {error_detail}")
        return response.json()