from typing import Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-04-15"

async def create_note(
    appointment_id: str,
    note_data: Dict[str, Any],
    headers: Dict[str, str]
) -> Dict[str, Any]:
    """
    Create a note for an appointment in Go High Level.
    
    Args:
        appointment_id: The ID of the appointment to add the note to
        note_data: Dictionary containing note details (userId, body)
        headers: Dictionary containing Authorization and Version headers
        
    Returns:
        Dictionary containing the created note data
        
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
    
    logging.info(f"Creating note for appointment: {appointment_id}")
    
    try:
        # Make the API request to create note
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                f"{API_BASE_URL}/calendars/appointments/{appointment_id}/notes",
                headers=request_headers,
                json=note_data
            )
            
        # Handle the API response
        if response.status_code != 201:
            error_detail = response.text
            logging.error(f"API request failed with status {response.status_code}: {error_detail}")
            raise Exception(f"API request failed with status {response.status_code}: {error_detail}")
            
        return response.json()
        
    except Exception as e:
        logging.error(f"Error creating note: {str(e)}")
        raise