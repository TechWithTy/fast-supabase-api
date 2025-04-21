from typing import Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def delete_field_folder(
    folder_id: str,
    location_id: str,
    headers: Dict[str, str]
) -> Dict[str, Any]:
    """
    Delete a custom field folder by ID from the Go High Level API.
    
    Args:
        folder_id: The ID of the folder to delete
        location_id: The location ID (Sub Account ID)
        headers: Dictionary containing Authorization and Version headers
        
    Returns:
        Dictionary containing success status and folder details
        
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
        "locationId": location_id
    }
    
    logging.info(f"Making request to delete custom field folder: {folder_id}")
    
    try:
        # Make the API request to delete the folder
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.delete(
                f"{API_BASE_URL}/custom-fields/folder/{folder_id}",
                params=params,
                headers=request_headers
            )
            
        # Handle the API response
        if response.status_code != 200:
            error_detail = response.text
            logging.error(f"API request failed with status {response.status_code}: {error_detail}")
            raise Exception(f"API request failed with status {response.status_code}: {error_detail}")
            
        return response.json()
        
    except Exception as e:
        logging.error(f"Error deleting custom field folder: {str(e)}")
        raise