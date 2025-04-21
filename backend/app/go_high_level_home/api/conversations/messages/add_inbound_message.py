from typing import Dict, Any, List, Optional
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-04-15"

async def add_inbound_message(
    headers: Dict[str, str],
    type: str,
    conversation_id: str,
    conversation_provider_id: str,
    message: Optional[str] = None,
    attachments: Optional[List[str]] = None,
    html: Optional[str] = None,
    subject: Optional[str] = None,
    email_from: Optional[str] = None,
    email_to: Optional[str] = None,
    email_cc: Optional[List[str]] = None,
    email_bcc: Optional[List[str]] = None,
    email_message_id: Optional[str] = None,
    alt_id: Optional[str] = None,
    direction: Optional[str] = "inbound",
    date: Optional[str] = None,
    call: Optional[Dict[str, Any]] = None,
    to: Optional[str] = None,
    from_: Optional[str] = None,
    status: Optional[str] = None
) -> Dict[str, Any]:
    """
    Add an inbound message to a conversation.
    
    Args:
        headers: Dictionary containing Authorization and Version headers
        type: Message type (SMS, Email, WhatsApp, GMB, IG, FB, Custom, WebChat, Live_Chat, Call)
        conversation_id: The ID of the conversation
        conversation_provider_id: The provider ID of the conversation
        message: Message body
        attachments: Array of attachment URLs
        html: HTML body of email
        subject: Subject of the email
        email_from: Sender email address
        email_to: Recipient email address
        email_cc: List of CC email addresses
        email_bcc: List of BCC email addresses
        email_message_id: Email message ID for threading
        alt_id: External mail provider's message ID
        direction: Message direction (inbound or outbound)
        date: Date of the inbound message
        call: Phone call information dictionary
        to: Phone number of the receiver
        from_: Phone number of the dialer
        status: Call status
        
    Returns:
        Dictionary containing response data with conversation and message details
        
    Raises:
        Exception: If the API request fails
    """
    # Validate required headers
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise Exception("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")
    
    if not headers.get("Version"):
        headers["Version"] = API_VERSION
    
    # Prepare request headers
    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers["Version"],
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    # Prepare request payload
    payload = {
        "type": type,
        "conversationId": conversation_id,
        "conversationProviderId": conversation_provider_id,
        "direction": direction
    }
    
    # Add optional fields to payload
    if message is not None:
        payload["message"] = message
    if attachments is not None:
        payload["attachments"] = attachments
    if html is not None:
        payload["html"] = html
    if subject is not None:
        payload["subject"] = subject
    if email_from is not None:
        payload["emailFrom"] = email_from
    if email_to is not None:
        payload["emailTo"] = email_to
    if email_cc is not None:
        payload["emailCc"] = email_cc
    if email_bcc is not None:
        payload["emailBcc"] = email_bcc
    if email_message_id is not None:
        payload["emailMessageId"] = email_message_id
    if alt_id is not None:
        payload["altId"] = alt_id
    if date is not None:
        payload["date"] = date
    
    # Add call information if provided
    if call is not None:
        payload["call"] = call
    elif to is not None and from_ is not None:
        payload["to"] = to
        payload["from"] = from_
        if status is not None:
            payload["status"] = status
    
    # Make API request
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_BASE_URL}/conversations/messages/inbound",
            headers=request_headers,
            json=payload
        )
    
    # Check for successful response
    if response.status_code != 200:
        logging.error(f"Failed to add inbound message: {response.text}")
        raise Exception(f"Failed to add inbound message: {response.status_code} - {response.text}")
    
    return response.json()