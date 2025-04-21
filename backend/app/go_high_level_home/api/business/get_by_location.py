from typing import Dict, Any, List
import httpx


async def get_business_by_location(
    location_id: str,
    headers: Dict[str, str]
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Get businesses by location from the Go High Level API.
    
    Args:
        location_id: The ID of the location to get businesses for
        headers: Dictionary containing Authorization and Version headers
        
    Returns:
        Dictionary containing the businesses data with a 'businesses' array
        
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
        headers["Version"] = "2021-07-28"
    
    # Prepare request headers
    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers["Version"],
        "Accept": "application/json"
    }
    
    # Prepare query parameters
    params = {"locationId": location_id}
    
    try:
        # Make the API request to get businesses
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                f"{API_BASE_URL}/businesses/",
                headers=request_headers,
                params=params
            )
            
        # Handle the API response
        if response.status_code != 200:
            error_detail = response.text
            raise Exception(f"API request failed with status {response.status_code}: {error_detail}")
        
        return response.json()
        
    except Exception as e:
        raise Exception(f"Failed to get businesses by location: {str(e)}")