from typing import Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def create_tag(location_id: str, tag_name: str, headers: Dict[str, str]) -> Dict[str, Any]:
    """
    Create a new tag for a specific location using the Go High Level API.

    Args:
        location_id: The ID of the location
        tag_name: The name of the tag to create
        headers: Dictionary containing Authorization and Version headers

    Returns:
        Dictionary containing the created tag data

    Raises:
        Exception: If the API request fails or if required headers are missing
    """
    url = f"{API_BASE_URL}/locations/{location_id}/tags"

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

    data = {"name": tag_name}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=request_headers, json=data)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {e}")
        raise Exception(f"Failed to create tag: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise Exception(f"An error occurred while creating tag: {e}")