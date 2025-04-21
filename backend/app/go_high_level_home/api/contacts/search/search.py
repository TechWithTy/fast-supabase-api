from typing import Dict, Any, List, Optional
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def search_contacts(
    headers: Dict[str, str],
    filters: Optional[Dict[str, Any]] = None,
    location_id: Optional[str] = None,
    limit: int = 20,
    offset: int = 0
) -> Dict[str, Any]:
    """
    Search contacts based on combinations of advanced filters.
    
    Args:
        headers: Dictionary containing Authorization and Version headers
        filters: Optional dictionary of filter criteria
        location_id: Optional location ID to filter contacts
        limit: Maximum number of results to return (default: 20)
        offset: Number of results to skip (default: 0)
        
    Returns:
        Dictionary containing contacts and total count
    """
    url = f"{API_BASE_URL}/contacts/search"
    
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    if not headers.get("Version"):
        headers["Version"] = API_VERSION

    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers["Version"],
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    payload = {
        "limit": limit,
        "offset": offset
    }
    
    if filters:
        payload["filters"] = filters
        
    if location_id:
        payload["locationId"] = location_id
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=request_headers, json=payload)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {e}")
        raise
    except Exception as e:
        logging.error(f"Error searching contacts: {e}")
        raise