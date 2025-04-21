# backend/apps/go_high_level/api/associations/delete.py
from typing import Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def delete_association(
    association_id: str,
    headers: Dict[str, str]
) -> Dict[str, Any]:
    """
    Delete a USER_DEFINED Association By Id.
    Deleting an association will also remove all the relations for that association.
    
    Args:
        association_id: The ID of the association to delete
        headers: Dictionary containing Authorization and Version headers
        
    Returns:
        Dictionary containing deletion status, association id and message
        
    Raises:
        Exception: If the API request fails or if required headers are missing
    """
    # Validate required headers
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise Exception("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    if not headers.get("Version"):
        # Set default version if not provided
        headers["Version"] = API_VERSION
    
    # Prepare request headers
    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers["Version"],
        "Accept": "application/json"
    }
    
    logging.info(f"Making request to delete association {association_id}")
    
    try:
        # Make the API request to delete the association
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.delete(
                f"{API_BASE_URL}/associations/{association_id}",
                headers=request_headers
            )
            
            if response.status_code != 200:
                error_message = response.text
                logging.error(f"Failed to delete association: {error_message}")
                raise Exception(f"Failed to delete association: {error_message}")
            
            return response.json()
            
    except httpx.RequestError as e:
        logging.error(f"Request error when deleting association: {str(e)}")
        raise Exception(f"Request error when deleting association: {str(e)}")