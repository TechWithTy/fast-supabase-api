from typing import Dict, Any, List, Optional
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-04-15"

async def add_external_call(
    headers: Dict[str, str],
    conversation_id: str,
    conversation_provider_id: str,
    to: str,
    from_: str,
    status: str = "completed",
    attachments: Optional[List[str]] = None,
    alt_id: Optional[str] = None,
    date: Optional[str] = None
) -> Dict[str, Any]:
    """
    Add an external outbound call to a conversation.
    
    Args:
        headers: Dictionary containing Authorization and Version headers
        conversation_id: The ID of the conversation
        conversation_provider_id: The provider ID of the conversation
        to: Phone number of the receiver
        from_: Phone number of the dialer
        status: Call status (pending, completed, answered, busy, no-answer, failed, canceled, voicemail)
        attachments: Array of attachment URLs
        alt_id: External mail provider's message ID
        date: Date of the outbound message in ISO format
        
    Returns:
        Dictionary containing response data with conversation and message details
        
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
        "type": "Call",
        "conversationId": conversation_id,
        "conversationProviderId": conversation_provider_id,
        "call": {
            "to": to,
            "from": from_,
            "status": status
        }
    }
    
    # Add optional parameters if provided
    if attachments:
        payload["attachments"] = attachments
    
    if alt_id:
        payload["altId"] = alt_id
    
    if date:
        payload["date"] = date
    
    logging.info(f"Adding external call to conversation: {conversation_id}")
    
    try:
        # Make the API request
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                f"{API_BASE_URL}/conversations/messages/outbound",
                headers=request_headers,
                json=payload
            )
            
            # Raise exception for non-2xx responses
            response.raise_for_status()
            
            # Return the response data
            return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {e}")
        raise Exception(f"Failed to add external call: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise Exception(f"Failed to add external call: {e}")