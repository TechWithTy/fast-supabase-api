from typing import Dict, Any, List
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def get_all_notes(contact_id: str, headers: Dict[str, str]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Get all notes for a contact in Go High Level.
    
    Args:
        contact_id: The ID of the contact
        headers: Dictionary containing Authorization and Version headers
        
    Returns:
        Dictionary containing the notes data with structure: {"notes": [...]}
        
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
    
    logging.info(f"Getting all notes for contact {contact_id}")
    
    try:
        # Make the API request to get all notes
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                f"{API_BASE_URL}/contacts/{contact_id}/notes",
                headers=request_headers
            )
            
        # Handle the API response
        if response.status_code != 200:
            error_message = f"Failed to get notes: {response.status_code} - {response.text}"
            logging.error(error_message)
            raise Exception(error_message)
            
        return response.json()
        
    except Exception as e:
        logging.error(f"Error getting notes for contact {contact_id}: {str(e)}")
        raise