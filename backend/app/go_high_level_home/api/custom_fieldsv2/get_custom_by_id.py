from typing import Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def get_custom_field_by_id(field_id: str, headers: Dict[str, str]) -> Dict[str, Any]:
    """
    Get Custom Field / Folder By Id.
    Only supports Custom Objects and Company (Business) today.
    
    Args:
        field_id: The ID of the custom field to retrieve
        headers: Dictionary containing Authorization and Version headers
        
    Returns:
        Dict containing the custom field data
    """
    url = f"{API_BASE_URL}/custom-fields/{field_id}"
    
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    request_headers = {
        "Accept": "application/json",
        "Authorization": headers["Authorization"],
        "Version": headers.get("Version", API_VERSION)
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=request_headers)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {e}")
        raise
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise