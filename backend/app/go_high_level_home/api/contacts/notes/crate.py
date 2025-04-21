from typing import Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def create_note(
    contact_id: str,
    body: str,
    headers: Dict[str, str],
    user_id: str = None
) -> Dict[str, Any]:
    """
    Create a note for a contact in Go High Level.
    
    Args:
        contact_id: The ID of the contact to add the note to
        body: The content of the note
        headers: Dictionary containing Authorization and Version headers
        user_id: Optional user ID associated with the note
        
    Returns:
        Dictionary containing the created note data
        
    Raises:
        Exception: If the API request fails or if required headers are missing
    """
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    if not headers.get("Version"):
        headers["Version"] = API_VERSION

    url = f"{API_BASE_URL}/contacts/{contact_id}/notes"
    
    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers["Version"],
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    payload = {"body": body}
    if user_id:
        payload["userId"] = user_id
    
    logging.info(f"Creating note for contact: {contact_id}")
    
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                url,
                headers=request_headers,
                json=payload
            )
            
        if response.status_code != 201:
            error_detail = response.text
            logging.error(f"API request failed with status {response.status_code}: {error_detail}")
            raise Exception(f"Failed to create note: {error_detail}")
            
        return response.json()
        
    except Exception as e:
        logging.error(f"Error creating note: {str(e)}")
        raise