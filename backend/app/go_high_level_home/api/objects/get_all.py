from typing import Dict, Any, List
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def get_all_objects(
    location_id: str,
    headers: Dict[str, str]
) -> Dict[str, Any]:
    """
    Get all objects for a location from the Go High Level API.
    
    Supported objects are contact, opportunity, business and custom objects.
    
    Args:
        location_id: The ID of the location to get objects for
        headers: Dictionary containing Authorization and Version headers
        
    Returns:
        Dictionary containing the objects data with an 'objects' array
        
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
    
    logging.info(f"Making request to get all objects for location: {location_id}")
    
    try:
        # Make the API request to get objects
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                f"{API_BASE_URL}/objects/",
                headers=request_headers,
                params=params
            )
            
        # Handle the API response
        if response.status_code != 200:
            error_detail = response.text
            logging.error(f"API request failed with status {response.status_code}: {error_detail}")
            raise Exception(f"API request failed with status {response.status_code}: {error_detail}")
            
        return response.json()
    except Exception as e:
        logging.error(f"Error getting objects: {str(e)}")
        raise