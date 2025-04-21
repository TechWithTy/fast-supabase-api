from typing import Dict, Any
import httpx
import logging

async def get_appointments(
    contact_id: str,
    headers: Dict[str, str]
) -> Dict[str, Any]:
    """
    Get appointments for a specific contact from the Go High Level API.
    
    Args:
        contact_id: The ID of the contact to get appointments for
        headers: Dictionary containing Authorization and Version headers
        
    Returns:
        Dictionary containing the appointments data with an 'events' array
        
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
        "Accept": "application/json"
    }
    
    logging.info(f"Making request to get appointments for contact: {contact_id}")
    
    try:
        # Make the API request to get appointments
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                f"{API_BASE_URL}/contacts/{contact_id}/appointments",
                headers=request_headers
            )
            
        # Handle the API response
        if response.status_code != 200:
            error_detail = response.text
            logging.error(f"API request failed with status {response.status_code}: {error_detail}")
            raise Exception(f"API request failed with status {response.status_code}: {error_detail}")
        
        appointments_data = response.json()
        logging.info(f"Successfully retrieved {len(appointments_data.get('events', []))} appointments")
        return appointments_data
        
    except httpx.RequestError as e:
        logging.error(f"Request error when fetching appointments: {str(e)}")
        raise Exception(f"Request error: {str(e)}")
    except Exception as e:
        logging.error(f"Error fetching appointments: {str(e)}")
        raise Exception(f"Error fetching appointments: {str(e)}")