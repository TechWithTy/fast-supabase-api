from typing import Dict, Any, List, Optional
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def get_all_associations_for_sub_account(
    location_id: str,
    headers: Dict[str, str],
    limit: int = 100,
    skip: int = 0
) -> Dict[str, Any]:
    """
    Get all associations for a sub-account/location from Go High Level API.
    
    Args:
        location_id: The ID of the location to get associations for
        headers: Dictionary containing Authorization and Version headers
        limit: Maximum number of associations to return (default: 100)
        skip: Number of records to skip for pagination (default: 0)
        
    Returns:
        Dictionary containing the associations data
        
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
        "limit": limit,
        "skip": skip
    }
    
    logging.info(f"Making request to get associations for location: {location_id}")
    
    try:
        # Make the API request to get associations
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                f"{API_BASE_URL}/associations/",
                headers=request_headers,
                params=params
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as exc:
        logging.error(f"HTTP error occurred: {exc.response.status_code} - {exc.response.text}")
        raise Exception(f"Failed to get associations: {exc.response.text}")
    except Exception as exc:
        logging.error(f"An error occurred: {str(exc)}")
        raise Exception(f"Failed to get associations: {str(exc)}")