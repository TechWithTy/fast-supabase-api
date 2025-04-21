from typing import Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def update_association_by_id(
    headers: Dict[str, str],
    association_id: str,
    first_object_label: str,
    second_object_label: str
) -> Dict[str, Any]:
    """
    Update association labels in Go High Level.
    
    Args:
        headers: Dictionary containing Authorization and Version headers
        association_id: The ID of the association to update
        first_object_label: New label for the first object
        second_object_label: New label for the second object
        
    Returns:
        Dictionary containing the updated association data
    """
    url = f"{API_BASE_URL}/associations/{association_id}"
    
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise Exception("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    if not headers.get("Version"):
        headers["Version"] = API_VERSION

    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers["Version"],
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    payload = {
        "firstObjectLabel": first_object_label,
        "secondObjectLabel": second_object_label
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.put(url, headers=request_headers, json=payload)
        
        if response.status_code != 200:
            logging.error(f"Failed to update association: {response.text}")
            response.raise_for_status()
            
        return response.json()