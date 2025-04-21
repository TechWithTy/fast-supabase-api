from typing import Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-04-15"

async def validate_group_slug(
    location_id: str,
    slug: str,
    headers: Dict[str, str]
) -> Dict[str, Any]:
    """
    Validate if a calendar group slug is available.
    
    Args:
        location_id: The ID of the location
        slug: The slug to validate
        headers: Dictionary containing Authorization and Version headers
        
    Returns:
        Dictionary with 'available' boolean indicating if slug is available
        
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
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    # Prepare request body
    request_body = {
        "locationId": location_id,
        "slug": slug
    }
    
    logging.info(f"Validating group slug '{slug}' for location: {location_id}")
    
    try:
        # Make the API request to validate the slug
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                f"{API_BASE_URL}/calendars/groups/validate-slug",
                headers=request_headers,
                json=request_body
            )
            
        # Handle the API response
        if response.status_code != 200:
            error_message = f"API request failed with status code {response.status_code}"
            try:
                error_data = response.json()
                error_message += f": {error_data.get('message', '')}"
            except Exception:
                pass
            raise Exception(error_message)
        
        return response.json()
    except httpx.RequestError as e:
        raise Exception(f"Request error: {str(e)}")