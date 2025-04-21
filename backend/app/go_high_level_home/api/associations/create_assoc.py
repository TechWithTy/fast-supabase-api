from typing import Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def create_association(
    token: str,
    location_id: str,
    key: str,
    first_object_label: str,
    first_object_key: str,
    second_object_label: str,
    second_object_key: str
) -> Dict[str, Any]:
    """
    Create an association between objects in Go High Level.
    
    Args:
        token: The authorization token
        location_id: The location ID
        key: Association's unique key
        first_object_label: First object's association label
        first_object_key: First object's key
        second_object_label: Second object's association label
        second_object_key: Second object's key
        
    Returns:
        Dictionary containing the created association data
    """
    url = f"{API_BASE_URL}/associations/"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Version": API_VERSION,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    payload = {
        "locationId": location_id,
        "key": key,
        "firstObjectLabel": first_object_label,
        "firstObjectKey": first_object_key,
        "secondObjectLabel": second_object_label,
        "secondObjectKey": second_object_key
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
        
        if response.status_code != 201:
            logging.error(f"Failed to create association: {response.text}")
            response.raise_for_status()
            
        return response.json()