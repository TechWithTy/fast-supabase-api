from typing import Dict, Any, List, Optional
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-04-15"

async def get_messages_by_conversation_id(
    conversation_id: str,
    headers: Dict[str, str],
    last_message_id: Optional[str] = None,
    limit: Optional[int] = 20,
    message_type: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get messages by conversation ID from the Go High Level API.
    
    Args:
        conversation_id: The ID of the conversation to retrieve messages from
        headers: Dictionary containing Authorization and Version headers
        last_message_id: Message ID of the last message in the list (for pagination)
        limit: Number of messages to fetch (default: 20)
        message_type: Types of messages to fetch (comma-separated)
        
    Returns:
        Dictionary containing messages, lastMessageId, and nextPage flag
        
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
    params = {}
    if last_message_id:
        params["lastMessageId"] = last_message_id
    if limit:
        params["limit"] = limit
    if message_type:
        params["type"] = message_type
    
    logging.info(f"Fetching messages for conversation: {conversation_id}")
    
    try:
        # Make the API request to get messages
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                f"{API_BASE_URL}/conversations/{conversation_id}/messages",
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
        logging.error(f"Error getting messages: {str(e)}")
        raise