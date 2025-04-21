from typing import Dict, Any, List, Optional
import httpx
import logging

async def get_free_slots(
    calendar_id: str,
    start_date: int,
    end_date: int,
    headers: Dict[str, str],
    enable_look_busy: Optional[bool] = False,
    timezone: Optional[str] = None,
    user_id: Optional[str] = None,
    user_ids: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Get free slots for a calendar between a date range.
    
    Args:
        calendar_id: The ID of the calendar
        start_date: Start date timestamp in milliseconds
        end_date: End date timestamp in milliseconds
        headers: Dictionary containing Authorization and Version headers
        enable_look_busy: Apply Look Busy feature, defaults to False
        timezone: The timezone in which the free slots are returned
        user_id: The user for whom the free slots are returned
        user_ids: The users for whom the free slots are returned
        
    Returns:
        Dictionary containing the free slots data with "_dates_" object containing "slots" array
        
    Raises:
        Exception: If the API request fails or if required headers are missing
    """
    # Define API base URL
    API_BASE_URL = "https://services.leadconnectorhq.com"
    
    # Validate required headers
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise Exception("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    if not headers.get("Version"):
        # Set default version if not provided
        headers["Version"] = "2021-04-15"
    
    # Prepare request headers
    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers["Version"],
        "Accept": "application/json"
    }
    
    # Prepare query parameters
    params = {
        "startDate": start_date,
        "endDate": end_date
    }
    
    if enable_look_busy is not None:
        params["enableLookBusy"] = enable_look_busy
        
    if timezone:
        params["timezone"] = timezone
        
    if user_id:
        params["userId"] = user_id
        
    if user_ids:
        params["userIds"] = user_ids
    
    logging.info(f"Making request to get free slots for calendar: {calendar_id}")
    
    try:
        # Make the API request to get free slots
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                f"{API_BASE_URL}/calendars/{calendar_id}/free-slots",
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
        logging.error(f"Error getting free slots: {str(e)}")
        raise