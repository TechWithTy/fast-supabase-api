from typing import Dict, Any, Optional
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def create_email_template(
    location_id: str,
    template_type: str,
    import_provider: str,
    headers: Dict[str, str],
    title: Optional[str] = None,
    updated_by: Optional[str] = None,
    builder_version: str = "2",
    name: Optional[str] = None,
    parent_id: Optional[str] = None,
    template_data_url: str = "",
    import_url: Optional[str] = None,
    template_source: Optional[str] = None,
    is_plain_text: bool = False
) -> Dict[str, Any]:
    """
    Create a new email template in Go High Level.
    
    Args:
        location_id: The ID of the location
        template_type: Template type (html, folder, import, builder, blank)
        import_provider: Provider for import (mailchimp, active_campaign, kajabi)
        headers: Dictionary containing Authorization and Version headers
        title: Title of the template
        updated_by: ID of the user who updated the template
        builder_version: Builder version, defaults to "2"
        name: Name of the template
        parent_id: ID of the parent template
        template_data_url: URL for template data
        import_url: URL to import template from
        template_source: Source of the template
        is_plain_text: Whether the template is plain text
        
    Returns:
        Dictionary containing the created template data
        
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
    template_data = {
        "locationId": location_id,
        "type": template_type,
        "importProvider": import_provider,
        "builderVersion": builder_version,
        "templateDataUrl": template_data_url,
        "isPlainText": is_plain_text
    }
    
    # Add optional fields if provided
    if title:
        template_data["title"] = title
    if updated_by:
        template_data["updatedBy"] = updated_by
    if name:
        template_data["name"] = name
    if parent_id:
        template_data["parentId"] = parent_id
    if import_url:
        template_data["importURL"] = import_url
    if template_source:
        template_data["templateSource"] = template_source
    
    logging.info("Creating email template")
    
    try:
        # Make the API request to create email template
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                f"{API_BASE_URL}/emails/builder",
                headers=request_headers,
                json=template_data
            )
            
        # Handle the API response
        if response.status_code != 201:
            error_detail = response.text
            logging.error(f"API request failed with status {response.status_code}: {error_detail}")
            raise Exception(f"API request failed with status {response.status_code}: {error_detail}")
        
        return response.json()
    
    except Exception as e:
        logging.error(f"Error creating email template: {str(e)}")
        raise