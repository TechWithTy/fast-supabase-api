from typing import Dict, Any, List, Optional
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-04-15"

async def update_calendar_notification(
    calendar_id: str,
    notification_id: str,
    notification_data: Dict[str, Any],
    headers: Dict[str, str]
) -> Dict[str, Any]:
    """
    Update a calendar notification in Go High Level.
    
    Args:
        calendar_id: The ID of the calendar
        notification_id: The ID of the notification to update
        notification_data: Dictionary containing notification details to update
        headers: Dictionary containing Authorization and Version headers
        
    Returns:
        Dictionary containing the updated notification data
        
    Raises:
        Exception: If the API request fails or if required headers are missing
    """
    # Validate required headers
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise Exception("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    if not headers.get("Version"):
        headers["Version"] = API_VERSION
    
    # Prepare request headers
    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers["Version"],
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    logging.info(f"Updating notification {notification_id} for calendar {calendar_id}")
    
    try:
        # Make the API request to update notification
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.put(
                f"{API_BASE_URL}/calendars/{calendar_id}/notifications/{notification_id}",
                headers=request_headers,
                json=notification_data
            )
            
        # Handle the API response
        if response.status_code != 200:
            error_detail = response.text
            logging.error(f"API request failed with status {response.status_code}: {error_detail}")
            raise Exception(f"Failed to update notification: {error_detail}")
            
        return response.json()
        
    except Exception as e:
        logging.error(f"Error updating calendar notification: {str(e)}")
        raise