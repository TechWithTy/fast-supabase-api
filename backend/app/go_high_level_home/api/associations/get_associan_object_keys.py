from typing import Dict, Any, Optional
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def get_association_by_object_key(
    headers: Dict[str, str],
    object_key: str,
    location_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get association by object keys like contacts, custom objects and opportunities.
    
    Args:
        headers: The request headers containing the authorization token
        object_key: The object key (e.g., custom_objects.car)
        location_id: Optional location ID
        
    Returns:
        Dictionary containing the association data
    """
    url = f"{API_BASE_URL}/associations/objectKey/{object_key}"
    
    headers.update({
        "Version": API_VERSION,
        "Accept": "application/json"
    })
    
    params = {}
    if location_id:
        params["locationId"] = location_id
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            logging.error(f"Failed to get association by object key: {response.text}")
            response.raise_for_status()
            
        return response.json()