from typing import Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-04-15"

async def get_calendar_notification(
    calendar_id: str,
    notification_id: str,
    headers: Dict[str, str]
) -> Dict[str, Any]:
    """
    Get a calendar notification by ID from the Go High Level API.
    
    Args:
        calendar_id: The ID of the calendar
        notification_id: The ID of the notification to retrieve
        headers: Dictionary containing Authorization and Version headers
        
    Returns:
        Dictionary containing the notification data
        
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
    
    logging.info(f"Making request to get calendar notification: {notification_id} for calendar: {calendar_id}")
    
    try:
        # Make the API request to get calendar notification
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                f"{API_BASE_URL}/calendars/{calendar_id}/notifications/{notification_id}",
                headers=request_headers
            )
            
        # Handle the API response
        if response.status_code != 200:
            error_detail = response.text
            logging.error(f"API request failed with status {response.status_code}: {error_detail}")
            raise Exception(f"API request failed with status {response.status_code}: {error_detail}")
            
        return response.json()
        
    except Exception as e:
        logging.error(f"Error getting calendar notification: {str(e)}")
        raise