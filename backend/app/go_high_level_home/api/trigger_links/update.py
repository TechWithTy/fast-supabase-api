from typing import Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def update_link(
    link_id: str,
    name: str,
    redirect_to: str,
    headers: Dict[str, str]
) -> Dict[str, Any]:
    """
    Update a link in Go High Level.

    Args:
        link_id: The ID of the link to update
        name: New name for the link
        redirect_to: New redirect URL for the link
        headers: Dictionary containing Authorization and Version headers

    Returns:
        Dictionary containing the updated link data

    Raises:
        Exception: If the API request fails or if required headers are missing
    """
    url = f"{API_BASE_URL}/links/{link_id}"

    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    if not headers.get("Version"):
        headers["Version"] = API_VERSION

    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers["Version"],
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    data = {
        "name": name,
        "redirectTo": redirect_to
    }

    async with httpx.AsyncClient() as client:
        response = await client.put(url, headers=request_headers, json=data)

        if response.status_code != 201:
            logging.error(f"Failed to update link: {response.text}")
            response.raise_for_status()

        return response.json()