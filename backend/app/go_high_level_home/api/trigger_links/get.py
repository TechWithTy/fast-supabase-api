from typing import Dict, Any, List
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def get_links(headers: Dict[str, str], location_id: str) -> List[Dict[str, Any]]:
    """
    Get links from the Go High Level API.

    Args:
        headers: Dictionary containing Authorization and Version headers
        location_id: The ID of the location

    Returns:
        A list of dictionaries containing link data

    Raises:
        Exception: If the API request fails or if required headers are missing
    """
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise Exception("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    if not headers.get("Version"):
        headers["Version"] = API_VERSION

    url = f"{API_BASE_URL}/links/"
    
    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers["Version"],
        "Accept": "application/json"
    }
    
    params = {
        "locationId": location_id
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=request_headers, params=params)
        
        if response.status_code != 200:
            logging.error(f"Failed to get links: {response.text}")
            response.raise_for_status()
        
        return response.json().get("links", [])