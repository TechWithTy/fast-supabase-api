from typing import Dict, Any, List
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-04-15"

async def upload_files(
    conversation_id: str,
    location_id: str,
    file_attachments: List[bytes],
    headers: Dict[str, str]
) -> Dict[str, Any]:
    """
    Upload file attachments to a conversation.
    
    Args:
        conversation_id: The ID of the conversation
        location_id: The ID of the location
        file_attachments: List of file attachments as bytes
        headers: Dictionary containing Authorization and Version headers
        
    Returns:
        Dictionary containing the uploaded files data
        
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
    
    # Prepare form data
    form_data = {
        "conversationId": conversation_id,
        "locationId": location_id
    }
    
    # Prepare files for upload
    files = []
    for i, file_attachment in enumerate(file_attachments):
        files.append(("fileAttachment", file_attachment))
    
    logging.info(f"Uploading files to conversation: {conversation_id}")
    
    try:
        # Make the API request to upload files
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                f"{API_BASE_URL}/conversations/messages/upload",
                headers=request_headers,
                data=form_data,
                files=files
            )
            
        # Handle the API response
        if response.status_code != 200:
            error_detail = response.text
            logging.error(f"File upload failed: {error_detail}")
            raise Exception(f"Failed to upload files: {error_detail}")
        
        return response.json()
        
    except Exception as e:
        logging.error(f"Error uploading files: {str(e)}")
        raise