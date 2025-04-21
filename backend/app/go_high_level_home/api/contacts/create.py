from typing import Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def create_contact(headers: Dict[str, str], **contact_data: Any) -> Dict[str, Any]:
    """
    Create a contact in Go High Level

    Args:
        headers (Dict[str, str]): Request headers including Authorization
        **contact_data: Contact data fields (firstName, lastName, etc.)

    Returns:
        Dict[str, Any]: API response

    Raises:
        ValueError: If Authorization header is missing or invalid
        Exception: If the API request fails
    """
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

    url = f"{API_BASE_URL}/contacts/"

    logging.info(f"Creating contact with data: {contact_data}")

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=request_headers, json=contact_data)

    if response.status_code != 200:
        logging.error(f"Failed to create contact. Status: {response.status_code}, Response: {response.text}")
        raise Exception(f"API request failed with status {response.status_code}: {response.text}")

    return response.json()