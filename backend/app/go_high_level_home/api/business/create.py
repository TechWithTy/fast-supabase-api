
from typing import Dict, Any
import httpx
import logging

async def create_appointment(
    contact_id: str,
    appointment_data: Dict[str, Any],
    headers: Dict[str, str]
) -> Dict[str, Any]:
    """
    Create an appointment for a specific contact in Go High Level.
    
    Args:
        contact_id: The ID of the contact to create appointment for
        appointment_data: Dictionary containing appointment details like title, startTime, etc.
        headers: Dictionary containing Authorization and Version headers
        
    Returns:
        Dictionary containing the created appointment data
        
    Raises:
        Exception: If the API request fails or if required headers are missing
    """
    # Define API base URL
    API_BASE_URL = "https://services.leadconnectorhq.com"
    
    # Validate required headers
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise Exception("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    if not headers.get("Version"):
        # Set default version if not provided
        headers["Version"] = "2021-07-28"
    
    # Prepare request headers
    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers["Version"],
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    logging.info(f"Creating appointment for contact: {contact_id}")
    
    try:
        # Make the API request to create appointment
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                f"{API_BASE_URL}/contacts/{contact_id}/appointments",
                headers=request_headers,
                json=appointment_data
            )
            
        # Handle the API response
        if response.status_code not in (200, 201):
            error_detail = response.text
            logging.error(f"API request failed with status {response.status_code}: {error_detail}")
            raise Exception(f"API request failed with status {response.status_code}: {error_detail}")
            
        return response.json()
    except Exception as e:
        logging.error(f"Error creating appointment: {str(e)}")
        raise