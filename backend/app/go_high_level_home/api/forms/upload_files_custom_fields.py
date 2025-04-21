from typing import Dict, Any, Optional, BinaryIO
import httpx
import logging
import uuid

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def upload_files_custom_fields(
    contact_id: str,
    location_id: str,
    files: Dict[str, BinaryIO],
    headers: Dict[str, str]
) -> Dict[str, Any]:
    """
    Upload files to custom fields for a contact.
    
    Args:
        contact_id: The ID of the contact
        location_id: Location ID of the contact
        files: Dictionary mapping custom_field_id to file objects
        headers: Dictionary containing Authorization and Version headers
        
    Returns:
        Dictionary containing the updated contact data
        
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
    params = {
        "contactId": contact_id,
        "locationId": location_id
    }
    
    # Prepare files for upload with format "custom_field_id_file_id"
    form_files = {}
    for custom_field_id, file_obj in files.items():
        file_id = str(uuid.uuid4())
        form_files[f"{custom_field_id}_{file_id}"] = file_obj
    
    logging.info(f"Uploading files for contact: {contact_id}")
    
    try:
        # Make the API request to upload files
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                f"{API_BASE_URL}/forms/upload-custom-files",
                headers=request_headers,
                params=params,
                files=form_files
            )
            
        # Handle the API response
        if response.status_code != 200:
            error_detail = response.text
            logging.error(f"API request failed with status {response.status_code}: {error_detail}")
            raise Exception(f"API request failed with status {response.status_code}: {error_detail}")
        
        return response.json()
    
    except httpx.RequestError as e:
        logging.error(f"Request error: {str(e)}")
        raise Exception(f"Request error: {str(e)}")