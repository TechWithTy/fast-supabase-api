from typing import Dict, Any, List, Optional
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-04-15"

async def list_calendar_resources(
    resource_type: str,
    location_id: str,
    headers: Dict[str, str],
    limit: int = 100,
    skip: int = 0
) -> Dict[str, Any]:
    """
    List calendar resources by resource type and location ID from Go High Level API.
    
    Args:
        resource_type: The type of resource ('equipments' or 'rooms')
        location_id: The location ID to get resources for
        headers: Dictionary containing Authorization and Version headers
        limit: Maximum number of resources to return
        skip: Number of resources to skip for pagination
        
    Returns:
        Dictionary containing the calendar resources data
        
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
    
    # Prepare query parameters
    params = {
        "locationId": location_id,
        "limit": limit,
        "skip": skip
    }
    
    logging.info(f"Making request to list calendar resources of type: {resource_type}")
    
    try:
        # Make the API request to list calendar resources
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                f"{API_BASE_URL}/calendars/resources/{resource_type}",
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
        logging.error(f"Error listing calendar resources: {str(e)}")
        raise