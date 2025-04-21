from typing import Dict, Any, List, Optional
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-04-15"

async def get_email(
    email_id: str,
    headers: Dict[str, str]
) -> Dict[str, Any]:
    """
    Get email message details from the Go High Level API.
    
    Args:
        email_id: The ID of the email message to retrieve
        headers: Dictionary containing Authorization and Version headers
        
    Returns:
        Dictionary containing the email message data
        
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
    
    logging.info(f"Making request to get email: {email_id}")
    
    try:
        # Make the API request to get email
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                f"{API_BASE_URL}/conversations/messages/email/{email_id}",
                headers=request_headers
            )
            
        # Handle the API response
        if response.status_code != 200:
            error_detail = response.text
            logging.error(f"API request failed with status {response.status_code}: {error_detail}")
            raise Exception(f"API request failed with status {response.status_code}: {error_detail}")
            
        return response.json()
        
    except httpx.HTTPError as e:
        logging.error(f"HTTP error occurred: {str(e)}")
        raise Exception(f"HTTP error occurred: {str(e)}")