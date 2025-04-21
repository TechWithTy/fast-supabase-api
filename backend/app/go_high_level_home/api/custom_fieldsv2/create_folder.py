from typing import Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def create_custom_field_folder(
    folder_data: Dict[str, Any],
    headers: Dict[str, str]
) -> Dict[str, Any]:
    """
    Create a custom field folder in Go High Level.
    
    Args:
        folder_data: Dictionary containing folder details (objectKey, name, locationId)
        headers: Dictionary containing Authorization and Version headers
        
    Returns:
        Dictionary containing the created custom field folder data
        
    Raises:
        Exception: If the API request fails or if required headers are missing
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
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    logging.info("Creating custom field folder")
    
    try:
        # Make the API request to create custom field folder
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                f"{API_BASE_URL}/custom-fields/folder",
                headers=request_headers,
                json=folder_data
            )
            
        # Handle the API response
        if response.status_code != 201:
            error_detail = response.text
            logging.error(f"API request failed with status {response.status_code}: {error_detail}")
            raise Exception(f"Failed to create custom field folder: {error_detail}")
        
        return response.json()
    except Exception as e:
        logging.error(f"Error creating custom field folder: {str(e)}")
        raise