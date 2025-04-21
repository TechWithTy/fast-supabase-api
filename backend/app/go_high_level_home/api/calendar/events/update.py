from typing import Dict, Any, Optional
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-04-15"

async def update_appointment(
    event_id: str,
    appointment_data: Dict[str, Any],
    headers: Dict[str, str]
) -> Dict[str, Any]:
    """
    Update an appointment by ID in Go High Level.
    
    Args:
        event_id: The ID of the event/appointment to update
        appointment_data: Dictionary containing appointment details to update
        headers: Dictionary containing Authorization and Version headers
        
    Returns:
        Dictionary containing the updated appointment data
        
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
    
    logging.info(f"Updating appointment with ID: {event_id}")
    
    try:
        # Make the API request to update appointment
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.put(
                f"{API_BASE_URL}/calendars/events/appointments/{event_id}",
                headers=request_headers,
                json=appointment_data
            )
            
        # Handle the API response
        if response.status_code != 200:
            error_detail = response.text
            logging.error(f"API request failed with status {response.status_code}: {error_detail}")
            raise Exception(f"API request failed with status {response.status_code}: {error_detail}")
        
        return response.json()
        
    except Exception as e:
        logging.error(f"Error updating appointment: {str(e)}")
        raise