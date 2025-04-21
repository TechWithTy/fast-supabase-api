from typing import Dict, Any, List, Optional
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-04-15"

async def create_calendar_resource(
    resource_type: str,
    location_id: str,
    name: str,
    description: str,
    headers: Dict[str, str],
    quantity: Optional[int] = None,
    out_of_service: Optional[int] = None,
    capacity: Optional[int] = None,
    calendar_ids: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Create a calendar resource in Go High Level.
    
    Args:
        resource_type: Resource type ('equipments' or 'rooms')
        location_id: Location ID for the resource
        name: Name of the resource
        description: Description of the resource
        headers: Dictionary containing Authorization and Version headers
        quantity: Quantity of the equipment
        out_of_service: Quantity of out of service equipment
        capacity: Capacity of the room
        calendar_ids: Service calendar IDs to map with the resource
        
    Returns:
        Dictionary containing the created calendar resource data
        
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
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    # Prepare request body
    request_body = {
        "locationId": location_id,
        "name": name,
        "description": description
    }
    
    if quantity is not None:
        request_body["quantity"] = quantity
    
    if out_of_service is not None:
        request_body["outOfService"] = out_of_service
    
    if capacity is not None:
        request_body["capacity"] = capacity
    
    if calendar_ids is not None:
        request_body["calendarIds"] = calendar_ids
    
    logging.info(f"Creating calendar resource of type: {resource_type}")
    
    try:
        # Make the API request to create calendar resource
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                f"{API_BASE_URL}/calendars/resources/{resource_type}",
                headers=request_headers,
                json=request_body
            )
            
        # Handle the API response
        if response.status_code != 201:
            error_detail = response.text
            logging.error(f"API request failed with status {response.status_code}: {error_detail}")
            raise Exception(f"API request failed with status {response.status_code}: {error_detail}")
            
        return response.json()
    
    except Exception as e:
        logging.error(f"Error creating calendar resource: {str(e)}")
        raise