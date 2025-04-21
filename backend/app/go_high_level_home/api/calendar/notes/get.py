from typing import Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-04-15"

async def get_notes(
    appointment_id: str,
    headers: Dict[str, str],
    limit: int = 10,
    offset: int = 0,
) -> Dict[str, Any]:
    """
    Get notes for an appointment in Go High Level.
    
    Args:
        appointment_id: The ID of the appointment to get notes for
        limit: Maximum number of notes to fetch (max 20)
        offset: Offset for pagination
        headers: Dictionary containing Authorization and Version headers
        
    Returns:
        Dictionary containing the appointment notes data
        
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
    
    # Prepare query parameters
    params = {
        "limit": min(limit, 20),  # Ensure limit doesn't exceed 20
        "offset": max(offset, 0)  # Ensure offset is not negative
    }
    
    logging.info(f"Getting notes for appointment: {appointment_id}")
    
    try:
        # Make the API request to get notes
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                f"{API_BASE_URL}/calendars/appointments/{appointment_id}/notes",
                headers=request_headers,
                params=params
            )
            
        # Handle the API response
        if response.status_code != 200:
            error_detail = response.text
            logging.error(f"API request failed with status {response.status_code}: {error_detail}")
            raise Exception(f"API request failed with status {response.status_code}: {error_detail}")
            
        return response.json()
        
    except Exception as e:
        logging.error(f"Error getting notes for appointment {appointment_id}: {str(e)}")
        raise