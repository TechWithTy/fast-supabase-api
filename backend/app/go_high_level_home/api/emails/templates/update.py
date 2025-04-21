from typing import Dict, Any, Optional
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def update_email_template(
    location_id: str,
    template_id: str,
    updated_by: str,
    headers: Dict[str, str],
    dnd: Dict[str, Any],
    html: str = "",
    editor_type: str = "html",
    preview_text: Optional[str] = None,
    is_plain_text: bool = False
) -> Dict[str, Any]:
    """
    Update an email template in Go High Level.
    
    Args:
        location_id: The ID of the location
        template_id: The ID of the template to update
        updated_by: ID of the user who updated the template
        headers: Dictionary containing Authorization and Version headers
        dnd: Template DND configuration
        html: HTML content of the template
        editor_type: Type of editor (html or builder)
        preview_text: Preview text for the email
        is_plain_text: Whether the template is plain text
        
    Returns:
        Dictionary containing the updated template data
        
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
        "templateId": template_id,
        "updatedBy": updated_by,
        "dnd": dnd,
        "html": html,
        "editorType": editor_type,
        "isPlainText": str(is_plain_text).lower()
    }
    
    if preview_text:
        payload["previewText"] = preview_text
    
    logging.info(f"Making request to update email template: {template_id}")
    
    try:
        # Make the API request to update template
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                f"{API_BASE_URL}/emails/builder/data",
                headers=request_headers,
                json=payload
            )
            
        # Handle the API response
        if response.status_code != 201:
            error_detail = response.text
            logging.error(f"API request failed with status {response.status_code}: {error_detail}")
            raise Exception(f"API request failed with status {response.status_code}: {error_detail}")
            
        return response.json()
    
    except httpx.RequestError as e:
        logging.error(f"Request error: {str(e)}")
        raise Exception(f"Request error: {str(e)}")