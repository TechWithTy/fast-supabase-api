from typing import Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-04-15"

async def send_typing_indicator(
    location_id: str,
    visitor_id: str,
    conversation_id: str,
    is_typing: bool,
    headers: Dict[str, str]
) -> Dict[str, Any]:
    """
    Send typing indicator for live chat.
    
    Args:
        location_id: The ID of the location
        visitor_id: The unique ID assigned to the live chat visitor
        conversation_id: The ID of the conversation
        is_typing: Typing status (True/False)
        headers: Dictionary containing Authorization and Version headers
        
    Returns:
        Dictionary containing the response data
        
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
        "isTyping": is_typing,
        "visitorId": visitor_id,
        "conversationId": conversation_id
    }
    
    logging.info(f"Sending typing indicator for conversation: {conversation_id}")
    
    try:
        # Make the API request
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                f"{API_BASE_URL}/conversations/providers/live-chat/typing",
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
        logging.error(f"Error sending typing indicator: {str(e)}")
        raise