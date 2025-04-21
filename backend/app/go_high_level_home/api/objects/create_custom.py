from typing import Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def create_custom_object(
    object_data: Dict[str, Any],
    headers: Dict[str, str]
) -> Dict[str, Any]:
    """
    Create a custom object schema in Go High Level.
    
    Args:
        object_data: Dictionary containing custom object details like labels, key,
                    description, locationId, primaryDisplayPropertyDetails, etc.
        headers: Dictionary containing Authorization and Version headers
        
    Returns:
        Dictionary containing the created custom object data
        
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
    
    logging.info("Creating custom object schema")
    
    try:
        # Make the API request to create custom object
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                f"{API_BASE_URL}/objects/",
                headers=request_headers,
                json=object_data
            )
            
        # Handle the API response
        if response.status_code != 201:
            error_detail = response.text
            logging.error(f"API request failed with status {response.status_code}: {error_detail}")
            raise Exception(f"API request failed with status {response.status_code}: {error_detail}")
            
        return response.json()
        
    except httpx.RequestError as e:
        logging.error(f"Request error occurred: {str(e)}")
        raise Exception(f"Request error occurred: {str(e)}")