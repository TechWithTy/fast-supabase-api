from typing import Dict, Any, Optional
import httpx
import logging

async def create_calendar_group(
    group_data: Dict[str, Any],
    headers: Dict[str, str]
) -> Dict[str, Any]:
    """
    Create a calendar group in Go High Level.
    
    Args:
        group_data: Dictionary containing group details (locationId, name, description, slug, isActive)
        headers: Dictionary containing Authorization and Version headers
        
    Returns:
        Dictionary containing the created calendar group data
        
    Raises:
        Exception: If the API request fails or if required headers are missing
    """
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
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    logging.info("Creating calendar group")
    
    try:
        # Make the API request to create calendar group
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                f"{API_BASE_URL}/calendars/groups",
                headers=request_headers,
                json=group_data
            )
            
        # Handle the API response
        if response.status_code != 201:
            error_detail = response.text
            logging.error(f"API request failed with status {response.status_code}: {error_detail}")
            raise Exception(f"API request failed with status {response.status_code}: {error_detail}")
            
        return response.json()
        
    except Exception as e:
        logging.error(f"Error creating calendar group: {str(e)}")
        raise