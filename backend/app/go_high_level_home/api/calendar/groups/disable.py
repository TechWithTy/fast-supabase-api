from typing import Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-04-15"

async def disable_calendar_group(
    group_id: str,
    is_active: bool,
    headers: Dict[str, str]
) -> Dict[str, Any]:
    """
    Enable or disable a calendar group in Go High Level.
    
    Args:
        group_id: The ID of the calendar group to update
        is_active: Boolean indicating whether the group should be active or not
        headers: Dictionary containing Authorization and Version headers
        
    Returns:
        Dictionary containing the response with success status
        
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
    
    # Prepare request body
    request_body = {
        "isActive": is_active
    }
    
    logging.info(f"Updating calendar group status: {group_id} to isActive={is_active}")
    
    try:
        # Make the API request to update group status
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.put(
                f"{API_BASE_URL}/calendars/groups/{group_id}/status",
                headers=request_headers,
                json=request_body
            )
            
        # Handle the API response
        if response.status_code != 200:
            error_detail = response.text
            logging.error(f"API request failed with status {response.status_code}: {error_detail}")
            raise Exception(f"Failed to update calendar group status: {error_detail}")
        
        return response.json()
        
    except httpx.RequestError as e:
        logging.error(f"Request error: {str(e)}")
        raise Exception(f"Network error while updating calendar group status: {str(e)}")