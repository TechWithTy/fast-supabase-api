from typing import Dict, Any, List
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def get_all_tasks(contact_id: str, headers: Dict[str, str]) -> Dict[str, Any]:
    """
    Get all tasks for a specific contact from the Go High Level API.
    
    Args:
        contact_id: The ID of the contact to get tasks for
        headers: Dictionary containing Authorization and Version headers
        
    Returns:
        Dict containing the tasks data
    """
    url = f"{API_BASE_URL}/contacts/{contact_id}/tasks"
    
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    if not headers.get("Version"):
        headers["Version"] = API_VERSION

    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers["Version"],
        "Accept": "application/json"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=request_headers)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {e}")
        raise
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise