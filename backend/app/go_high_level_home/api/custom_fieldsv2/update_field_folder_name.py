from typing import Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def update_field_folder_name(
    folder_id: str,
    folder_data: Dict[str, Any],
    headers: Dict[str, str]
) -> Dict[str, Any]:
    """
    Update a custom field folder name in Go High Level.
    
    Args:
        folder_id: The ID of the custom field folder to update
        folder_data: Dictionary containing folder details (name, locationId)
        headers: Dictionary containing Authorization and Version headers
        
    Returns:
        Dictionary containing the updated folder data
        
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
    
    logging.info(f"Updating custom field folder with ID: {folder_id}")
    
    try:
        # Make the API request to update field folder
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.put(
                f"{API_BASE_URL}/custom-fields/folder/{folder_id}",
                headers=request_headers,
                json=folder_data
            )
            
        # Handle the API response
        if response.status_code != 200:
            error_detail = response.text
            logging.error(f"API request failed with status {response.status_code}: {error_detail}")
            raise Exception(f"Failed to update field folder: {error_detail}")
            
        return response.json()
        
    except Exception as e:
        logging.error(f"Error updating field folder: {str(e)}")
        raise