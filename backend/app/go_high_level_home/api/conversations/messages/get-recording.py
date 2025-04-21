from typing import Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-04-15"

async def get_recording(
    message_id: str,
    location_id: str,
    headers: Dict[str, str]
) -> bytes:
    """
    Get the recording for a message by message ID.
    
    Args:
        message_id: The ID of the message
        location_id: The ID of the location
        headers: Dictionary containing Authorization and Version headers
        
    Returns:
        Binary content of the recording file
        
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
    
    logging.info(f"Fetching recording for message: {message_id} in location: {location_id}")
    
    try:
        # Make the API request to get the recording
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                f"{API_BASE_URL}/conversations/messages/{message_id}/locations/{location_id}/recording",
                headers=request_headers
            )
            
        # Handle the API response
        if response.status_code != 200:
            error_detail = response.text
            logging.error(f"API request failed with status {response.status_code}: {error_detail}")
            raise Exception(f"API request failed with status {response.status_code}: {error_detail}")
            
        return response.content
        
    except httpx.RequestError as e:
        logging.error(f"Request error: {str(e)}")
        raise Exception(f"Request error: {str(e)}")