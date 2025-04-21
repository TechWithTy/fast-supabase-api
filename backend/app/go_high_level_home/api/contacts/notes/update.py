from typing import Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def update_note(
    contact_id: str,
    note_id: str,
    note_data: Dict[str, Any],
    headers: Dict[str, str]
) -> Dict[str, Any]:
    """
    Update a note for a contact in Go High Level.
    
    Args:
        contact_id: The ID of the contact
        note_id: The ID of the note to update
        note_data: Dictionary containing note details (userId, body)
        headers: Dictionary containing Authorization and Version headers
        
    Returns:
        Dictionary containing the updated note data
        
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
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    logging.info(f"Updating note {note_id} for contact {contact_id}")
    
    try:
        # Make the API request to update note
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.put(
                f"{API_BASE_URL}/contacts/{contact_id}/notes/{note_id}",
                headers=request_headers,
                json=note_data
            )
            
        # Handle the API response
        if response.status_code != 200:
            error_detail = response.text
            logging.error(f"API request failed with status {response.status_code}: {error_detail}")
            raise Exception(f"API request failed with status {response.status_code}: {error_detail}")
            
        return response.json()
    
    except Exception as e:
        logging.error(f"Error updating note: {str(e)}")
        raise