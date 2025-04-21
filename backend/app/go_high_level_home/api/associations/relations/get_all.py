from typing import Dict, Any, List, Optional
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def get_all_relations(
    record_id: str,
    headers: Dict[str, str],
    location_id: str,
    limit: int = 100,
    skip: int = 0,
    association_ids: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Get all relations by record ID from Go High Level API.
    
    Args:
        record_id: The ID of the record to get relations for
        headers: Dictionary containing Authorization and Version headers
        location_id: The location ID (Sub-Account ID)
        limit: Maximum number of relations to return (default: 100)
        skip: Number of records to skip for pagination (default: 0)
        association_ids: Optional list of association IDs to filter by
        
    Returns:
        Dictionary containing the relations data
        
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
    
    if association_ids:
        params["associationIds"] = association_ids
    
    logging.info(f"Making request to get relations for record: {record_id}")
    
    try:
        # Make the API request to get relations
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                f"{API_BASE_URL}/associations/relations/{record_id}",
                headers=request_headers,
                params=params
            )
            
            if response.status_code != 200:
                error_message = response.text
                logging.error(f"Failed to get relations: {error_message}")
                raise Exception(f"Failed to get relations: {error_message}")
            
            return response.json()
            
    except Exception as e:
        logging.error(f"Error fetching relations: {str(e)}")
        raise