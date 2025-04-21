from typing import Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-04-15"

async def get_calendar_resource(
    resource_id: str,
    resource_type: str,
    headers: Dict[str, str]
) -> Dict[str, Any]:
    """
    Get a calendar resource by ID from the Go High Level API.
    
    Args:
        resource_id: The ID of the calendar resource
        resource_type: The type of resource ('equipments' or 'rooms')
        headers: Dictionary containing Authorization and Version headers
        
    Returns:
        Dictionary containing the calendar resource data
        
    Raises:
        Exception: If the API request fails or if required headers are missing
    """
    # Validate resource type
    if resource_type not in ["equipments", "rooms"]:
        raise ValueError("Resource type must be either 'equipments' or 'rooms'")
    
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
    
    logging.info(f"Making request to get calendar resource: {resource_id} of type: {resource_type}")
    
    try:
        # Make the API request to get the calendar resource
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                f"{API_BASE_URL}/calendars/resources/{resource_type}/{resource_id}",
                headers=request_headers
            )
            
        # Handle the API response
        if response.status_code != 200:
            error_detail = response.text
            logging.error(f"API request failed with status {response.status_code}: {error_detail}")
            raise Exception(f"API request failed with status {response.status_code}: {error_detail}")
            
        return response.json()
        
    except Exception as e:
        logging.error(f"Failed to get calendar resource: {str(e)}")
        raise