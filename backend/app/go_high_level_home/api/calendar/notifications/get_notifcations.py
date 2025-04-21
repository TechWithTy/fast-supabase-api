from typing import Dict, Any, Optional, List
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-04-15"

async def get_calendar_notifications(
    calendar_id: str,
    headers: Dict[str, str],
    alt_id: Optional[str] = None,
    alt_type: Optional[str] = "calendar",
    deleted: Optional[bool] = None,
    is_active: Optional[bool] = None,
    limit: Optional[int] = 100,
    skip: Optional[int] = 0
) -> Dict[str, Any]:
    """
    Get calendar notifications from the Go High Level API.
    
    Args:
        calendar_id: The ID of the calendar
        headers: Dictionary containing Authorization and Version headers
        alt_id: Specifies the ID of the model associated with the notification
        alt_type: Specifies the model associated with the notification (default: calendar)
        deleted: Filter by deleted status
        is_active: Filter by active status
        limit: Maximum number of records to return (default: 100)
        skip: Number of records to skip (default: 0)
        
    Returns:
        Dictionary containing the calendar notifications data
        
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
    
    # Prepare query parameters
    params = {}
    if alt_id:
        params["altId"] = alt_id
    if alt_type:
        params["altType"] = alt_type
    if deleted is not None:
        params["deleted"] = deleted
    if is_active is not None:
        params["isActive"] = is_active
    if limit:
        params["limit"] = limit
    if skip:
        params["skip"] = skip
    
    logging.info(f"Making request to get calendar notifications for calendar: {calendar_id}")
    
    try:
        # Make the API request to get calendar notifications
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                f"{API_BASE_URL}/calendars/{calendar_id}/notifications",
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
        logging.error(f"Error getting calendar notifications: {str(e)}")
        raise