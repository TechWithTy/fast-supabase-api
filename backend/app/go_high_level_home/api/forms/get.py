from typing import Dict, Any, Optional
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def get_forms(
    location_id: str,
    headers: Dict[str, str],
    limit: Optional[int] = 10,
    skip: Optional[int] = 0,
    form_type: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get forms from the Go High Level API.
    
    Args:
        location_id: The ID of the location to get forms for
        headers: Dictionary containing Authorization and Version headers
        limit: Maximum number of forms to fetch (default: 10, max: 50)
        skip: Number of forms to skip for pagination
        form_type: Type of form to filter by (e.g., 'folder')
        
    Returns:
        Dictionary containing the forms data
        
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
        "locationId": location_id,
        "limit": min(limit, 50),  # Ensure limit doesn't exceed 50
        "skip": skip
    }
    
    # Add optional form type parameter if provided
    if form_type:
        params["type"] = form_type
    
    logging.info(f"Getting forms for location: {location_id}")
    
    try:
        # Make the API request
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                f"{API_BASE_URL}/forms/",
                headers=request_headers,
                params=params
            )
            
            response.raise_for_status()
            return response.json()
            
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {e}")
        raise Exception(f"Failed to get forms: {str(e)}")
    except Exception as e:
        logging.error(f"Error getting forms: {e}")
        raise Exception(f"Failed to get forms: {str(e)}")