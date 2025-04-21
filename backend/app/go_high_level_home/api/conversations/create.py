from typing import Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-04-15"

async def create_conversation(
    location_id: str,
    contact_id: str,
    headers: Dict[str, str]
) -> Dict[str, Any]:
    """
    Create a new conversation in Go High Level.
    
    Args:
        location_id: The ID of the location
        contact_id: The ID of the contact
        headers: Dictionary containing Authorization and Version headers
        
    Returns:
        Dictionary containing the created conversation data
        
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
    
    # Prepare request payload
    payload = {
        "locationId": location_id,
        "contactId": contact_id
    }
    
    logging.info(f"Creating conversation for contact: {contact_id} in location: {location_id}")
    
    try:
        # Make the API request to create conversation
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                f"{API_BASE_URL}/conversations/",
                headers=request_headers,
                json=payload
            )
            
        # Handle the API response
        if response.status_code != 201:
            error_detail = response.text
            logging.error(f"API request failed with status {response.status_code}: {error_detail}")
            raise Exception(f"API request failed with status {response.status_code}: {error_detail}")
            
        return response.json()
        
    except Exception as e:
        logging.error(f"Error creating conversation: {str(e)}")
        raise