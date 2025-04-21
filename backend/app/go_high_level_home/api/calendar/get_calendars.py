from typing import Dict, Any, Optional
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-04-15"

async def get_calendars(
    location_id: str,
    headers: Dict[str, str],
    group_id: Optional[str] = None,
    show_drafted: Optional[bool] = True
) -> Dict[str, Any]:
    """
    Get all calendars in a location from the Go High Level API.
    
    Args:
        location_id: The ID of the location to get calendars for
        headers: Dictionary containing Authorization and Version headers
        group_id: Optional group ID to filter calendars by
        show_drafted: Whether to include drafted calendars, defaults to True
        
    Returns:
        Dictionary containing the calendars data with a 'calendars' array
        
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
    params = {
        "locationId": location_id
    }
    
    # Add optional parameters if provided
    if group_id:
        params["groupId"] = group_id
    
    if show_drafted is not None:
        params["showDrafted"] = str(show_drafted).lower()
    
    logging.info(f"Making request to get calendars for location: {location_id}")
    
    try:
        # Make the API request to get calendars
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                f"{API_BASE_URL}/calendars/",
                headers=request_headers,
                params=params
            )
            
        # Handle the API response
        if response.status_code != 200:
            error_detail = response.text
            logging.error(f"API request failed with status {response.status_code}: {error_detail}")
            raise Exception(f"API request failed with status {response.status_code}: {error_detail}")
            
        return response.json()
        
    except httpx.RequestError as e:
        logging.error(f"Request error occurred: {str(e)}")
        raise Exception(f"Request error: {str(e)}")