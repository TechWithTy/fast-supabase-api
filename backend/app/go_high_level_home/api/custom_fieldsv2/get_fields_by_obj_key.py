from typing import Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def get_fields_by_obj_key(
    headers: Dict[str, str],
    object_key: str,
    location_id: str
) -> Dict[str, Any]:
    """
    Get Custom Fields By Object Key.
    
    Only supports Custom Objects and Company (Business) today.
    
    Args:
        headers: Dictionary containing Authorization and Version headers
        object_key: Key of the Object (must include "custom_objects." prefix for custom objects)
        location_id: Location ID
        
    Returns:
        Dictionary containing custom fields data for the object
        
    Raises:
        Exception: If the API request fails or if required headers are missing
    """
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise Exception("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    if not headers.get("Version"):
        headers["Version"] = API_VERSION

    url = f"{API_BASE_URL}/custom-fields/object-key/{object_key}"
    
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
            logging.error(f"Failed to get custom fields: {response.text}")
            response.raise_for_status()
            
        return response.json()