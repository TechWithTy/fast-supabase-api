from typing import Dict, Any, List, Optional
import requests

def update_calendar_resource(
    resource_id: str,
    resource_type: str,
    access_token: str,
    location_id: str,
    name: str,
    description: Optional[str] = None,
    quantity: Optional[int] = None,
    out_of_service: Optional[int] = None,
    capacity: Optional[int] = None,
    calendar_ids: Optional[List[str]] = None,
    is_active: bool = True
) -> Dict[str, Any]:
    """
    Update a calendar resource by ID in Go High Level.
    
    Args:
        resource_id: The ID of the resource to update
        resource_type: Resource type ('equipments' or 'rooms')
        access_token: The access token for authentication
        location_id: Location ID of the resource
        name: Name of the resource
        description: Description of the resource
        quantity: Quantity of the equipment
        out_of_service: Quantity of out of service equipment
        capacity: Capacity of the room
        calendar_ids: Service calendar IDs to map with the resource
        is_active: Whether the resource is active
        
    Returns:
        Dict: The updated calendar resource data
    """
    url = f"https://services.leadconnectorhq.com/calendars/resources/{resource_type}/{resource_id}"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Version": "2021-04-15",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    data = {
        "locationId": location_id,
        "name": name,
        "isActive": is_active
    }
    
    if description is not None:
        data["description"] = description
    
    if quantity is not None:
        data["quantity"] = quantity
    
    if out_of_service is not None:
        data["outOfService"] = out_of_service
    
    if capacity is not None:
        data["capacity"] = capacity
    
    if calendar_ids is not None:
        data["calendarIds"] = calendar_ids
    
    response = requests.put(url, headers=headers, json=data)
    return response.json()