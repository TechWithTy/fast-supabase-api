from typing import Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-04-15"

async def get_transcription(
    location_id: str,
    message_id: str,
    headers: Dict[str, str]
) -> Dict[str, Any]:
    """
    Get transcription for a message by ID from the Go High Level API.
    
    Args:
        location_id: The ID of the location
        message_id: The ID of the message to retrieve transcription for
        headers: Dictionary containing Authorization and Version headers
        
    Returns:
        Dictionary containing the transcription data
        
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
    
    logging.info(f"Making request to get transcription for message: {message_id}")
    
    try:
        # Make the API request to get transcription
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                f"{API_BASE_URL}/conversations/locations/{location_id}/messages/{message_id}/transcription",
                headers=request_headers
            )
            
        # Handle the API response
        if response.status_code != 200:
            error_detail = response.text
            logging.error(f"API request failed with status {response.status_code}: {error_detail}")
            raise Exception(f"API request failed with status {response.status_code}: {error_detail}")
            
        return response.json()
        
    except Exception as e:
        logging.error(f"Error getting transcription: {str(e)}")
        raise