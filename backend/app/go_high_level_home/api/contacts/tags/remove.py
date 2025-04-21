from typing import Dict, Any, List
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def remove_contact_tags(
    contact_id: str,
    tags: List[str],
    headers: Dict[str, str]
) -> Dict[str, Any]:
    """
    Remove tags from a contact in Go High Level API.
    
    Args:
        contact_id: The ID of the contact
        tags: List of tag names to remove from the contact
        headers: Dictionary containing Authorization and Version headers
        
    Returns:
        Dictionary containing the updated tags
        
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
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    # Prepare request body
    request_body = {
        "tags": tags
    }
    
    logging.info(f"Making request to remove tags from contact: {contact_id}")
    
    try:
        # Make the API request to remove tags
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.delete(
                f"{API_BASE_URL}/contacts/{contact_id}/tags",
                headers=request_headers,
                json=request_body
            )
            
        # Handle the API response
        if response.status_code != 200:
            error_detail = response.text
            logging.error(f"API request failed with status {response.status_code}: {error_detail}")
            raise Exception(f"API request failed with status {response.status_code}: {error_detail}")
            
        return response.json()
    except Exception as e:
        logging.error(f"Error removing tags: {str(e)}")
        raise