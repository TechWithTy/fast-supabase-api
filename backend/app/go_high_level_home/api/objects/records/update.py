from typing import Dict, Any, List, Optional
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def update_record(
    schema_key: str,
    record_id: str,
    properties: Dict[str, Any],
    location_id: str,
    headers: Dict[str, str],
    owner: Optional[List[str]] = None,
    followers: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Update a Custom Object Record by Id. Supported Objects are business and custom objects.
    
    Args:
        schema_key: The key of the Custom Object / Standard Object Schema
        record_id: ID of the record to be updated
        properties: Properties of the record to update
        location_id: Location ID
        headers: Dictionary containing Authorization and Version headers
        owner: Owner (User's id). Limited to 1 for now. Only supported with custom objects
        followers: Follower (User's ids). Limited to 10 for now
        
    Returns:
        Dict containing the updated record information
    """
    url = f"{API_BASE_URL}/objects/{schema_key}/records/{record_id}"
    
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers.get("Version", API_VERSION),
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    params = {"locationId": location_id}
    
    payload = {"properties": properties}
    if owner:
        payload["owner"] = owner
    if followers:
        payload["followers"] = followers
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.put(url, headers=request_headers, params=params, json=payload)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {e}")
        raise
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise