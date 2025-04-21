from typing import Dict, Any, List, Optional
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-04-15"

async def create_calendar_notification(
    calendar_id: str,
    notifications: List[Dict[str, Any]],
    headers: Dict[str, str]
) -> List[Dict[str, Any]]:
    """
    Create calendar notifications in Go High Level.
    
    Args:
        calendar_id: ID of the calendar
        notifications: List of notification objects with properties like receiverType, 
                      channel, notificationType, etc.
        headers: Dictionary containing Authorization and Version headers
        
    Returns:
        List of created notification objects
        
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
    
    logging.info(f"Creating calendar notifications for calendar ID: {calendar_id}")
    
    try:
        # Make the API request to create calendar notifications
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                f"{API_BASE_URL}/calendars/{calendar_id}/notifications",
                headers=request_headers,
                json=notifications
            )
            
        # Handle the API response
        if response.status_code != 200:
            error_detail = response.text
            logging.error(f"API request failed with status {response.status_code}: {error_detail}")
            raise Exception(f"Failed to create calendar notifications: {error_detail}")
            
        return response.json()
        
    except Exception as e:
        logging.error(f"Error creating calendar notifications: {str(e)}")
        raise