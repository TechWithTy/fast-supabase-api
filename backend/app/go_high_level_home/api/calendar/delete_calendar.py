from typing import Dict, Any
import httpx
import logging

async def delete_calendar(
    calendar_id: str,
    headers: Dict[str, str]
) -> Dict[str, bool]:
    """
    Delete a calendar by ID from the Go High Level API.
    
    Args:
        calendar_id: The ID of the calendar to delete
        headers: Dictionary containing Authorization and Version headers
        
    Returns:
        Dictionary containing success status
        
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
    
    logging.info(f"Making request to delete calendar: {calendar_id}")
    
    try:
        # Make the API request to delete calendar
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.delete(
                f"{API_BASE_URL}/calendars/{calendar_id}",
                headers=request_headers
            )
            
        # Handle the API response
        if response.status_code != 200:
            error_detail = response.text
            logging.error(f"API request failed with status {response.status_code}: {error_detail}")
            raise Exception(f"API request failed with status {response.status_code}: {error_detail}")
            
        return response.json()
        
    except Exception as e:
        logging.error(f"Error deleting calendar: {str(e)}")
        raise