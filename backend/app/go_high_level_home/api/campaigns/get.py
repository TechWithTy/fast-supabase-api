from typing import Dict, Any, List, Optional
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def get_campaigns(
    location_id: str,
    headers: Dict[str, str],
    status: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get campaigns from the Go High Level API.
    
    Args:
        location_id: The ID of the location to get campaigns for
        headers: Dictionary containing Authorization and Version headers
        status: Optional status filter (e.g., 'draft', 'published')
        
    Returns:
        Dictionary containing the campaigns data with a 'campaigns' array
        
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
    
    if status:
        params["status"] = status
    
    logging.info(f"Making request to get campaigns for location: {location_id}")
    
    try:
        # Make the API request to get campaigns
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                f"{API_BASE_URL}/campaigns/",
                headers=request_headers,
                params=params
            )
            
        # Handle the API response
        if response.status_code != 200:
            error_detail = response.text
            logging.error(f"API request failed with status {response.status_code}: {error_detail}")
            raise Exception(f"API request failed with status {response.status_code}: {error_detail}")
            
        # Return the JSON response
        return response.json()
    
    except httpx.RequestError as e:
        logging.error(f"Request error: {str(e)}")
        raise Exception(f"Request error: {str(e)}")