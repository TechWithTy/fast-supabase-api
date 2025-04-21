from typing import Dict, Any, Optional, List
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-04-15"

async def get_blocked_slots(
    query_params: Dict[str, Any],
    headers: Dict[str, str]
) -> Dict[str, Any]:
    """
    Get blocked slots from the Go High Level API.
    
    Args:
        query_params: Dictionary containing query parameters (locationId, startTime, endTime, 
                     calendarId, groupId, or userId)
        headers: Dictionary containing Authorization and Version headers
        
    Returns:
        Dictionary containing the blocked slots data with 'events' array
        
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
    
    logging.info("Making request to get blocked slots")
    
    try:
        # Make the API request to get blocked slots
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                f"{API_BASE_URL}/calendars/blocked-slots",
                headers=request_headers,
                params=query_params
            )
            
        # Handle the API response
        if response.status_code != 200:
            error_detail = response.text
            logging.error(f"API request failed with status {response.status_code}: {error_detail}")
            raise Exception(f"API request failed with status {response.status_code}: {error_detail}")
            
        return response.json()
        
    except Exception as e:
        logging.error(f"Error getting blocked slots: {str(e)}")
        raise