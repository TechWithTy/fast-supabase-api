from typing import Dict, Any, Optional
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-04-15"

async def update_calendar_group(
    group_id: str,
    group_data: Dict[str, Any],
    headers: Dict[str, str]
) -> Dict[str, Any]:
    """
    Update a calendar group in Go High Level.
    
    Args:
        group_id: The ID of the calendar group to update
        group_data: Dictionary containing group details (name, description, slug)
        headers: Dictionary containing Authorization and Version headers
        
    Returns:
        Dictionary containing the updated calendar group data
        
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
    
    logging.info(f"Updating calendar group with ID: {group_id}")
    
    try:
        # Make the API request to update calendar group
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.put(
                f"{API_BASE_URL}/calendars/groups/{group_id}",
                headers=request_headers,
                json=group_data
            )
            
        # Handle the API response
        if response.status_code != 200:
            error_detail = response.text
            logging.error(f"API request failed with status {response.status_code}: {error_detail}")
            raise Exception(f"Failed to update calendar group: {error_detail}")
            
        return response.json()
        
    except Exception as e:
        logging.error(f"Error updating calendar group: {str(e)}")
        raise