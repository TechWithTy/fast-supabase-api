from typing import Dict, Any, List, Optional
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-04-15"

async def update_message_status(
    message_id: str,
    status: str,
    headers: Dict[str, str],
    error: Optional[Dict[str, str]] = None,
    email_message_id: Optional[str] = None,
    recipients: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Update the status of a message in Go High Level.
    
    Args:
        message_id: The ID of the message to update
        status: Message status (delivered, failed, pending, read)
        headers: Dictionary containing Authorization and Version headers
        error: Optional error object from the conversation provider
        email_message_id: Optional email message ID
        recipients: Optional list of email delivery status recipients
        
    Returns:
        Dictionary containing the updated message data
        
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
    
    # Prepare request body
    request_body = {
        "status": status
    }
    
    if error:
        request_body["error"] = error
    
    if email_message_id:
        request_body["emailMessageId"] = email_message_id
    
    if recipients:
        request_body["recipients"] = recipients
    
    logging.info(f"Updating status for message: {message_id}")
    
    try:
        # Make the API request to update message status
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.put(
                f"{API_BASE_URL}/conversations/messages/{message_id}/status",
                headers=request_headers,
                json=request_body
            )
            
        # Handle the API response
        if response.status_code != 200:
            error_detail = response.text
            logging.error(f"API request failed with status {response.status_code}: {error_detail}")
            raise Exception(f"API request failed with status {response.status_code}: {error_detail}")
            
        return response.json()
        
    except Exception as e:
        logging.error(f"Error updating message status: {str(e)}")
        raise