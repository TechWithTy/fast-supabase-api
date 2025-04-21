from typing import Dict, Any, List, Optional
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def create_custom_field(
    field_data: Dict[str, Any],
    headers: Dict[str, str]
) -> Dict[str, Any]:
    """
    Create a custom field in Go High Level.
    
    Args:
        field_data: Dictionary containing field details such as locationId, name,
                   description, dataType, fieldKey, objectKey, etc.
        headers: Dictionary containing Authorization and Version headers
        
    Returns:
        Dictionary containing the created custom field data
        
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
    
    logging.info("Creating custom field")
    
    try:
        # Make the API request to create custom field
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                f"{API_BASE_URL}/custom-fields/",
                headers=request_headers,
                json=field_data
            )
            
        # Handle the API response
        if response.status_code != 201:
            error_detail = response.text
            logging.error(f"API request failed with status {response.status_code}: {error_detail}")
            raise Exception(f"API request failed with status {response.status_code}: {error_detail}")
            
        return response.json()
        
    except Exception as e:
        logging.error(f"Error creating custom field: {str(e)}")
        raise