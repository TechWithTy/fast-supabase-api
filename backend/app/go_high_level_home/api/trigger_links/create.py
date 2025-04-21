from typing import Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def create_trigger_link(
    headers: Dict[str, str],
    location_id: str,
    name: str,
    redirect_to: str
) -> Dict[str, Any]:
    """
    Create a trigger link in Go High Level.
    
    Args:
        headers: Dictionary containing Authorization and Version headers
        location_id: The location ID
        name: Name of the trigger link
        redirect_to: URL to redirect to
        
    Returns:
        Dictionary containing the created trigger link data
    """
    url = f"{API_BASE_URL}/links/"
    
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers.get("Version", API_VERSION),
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    payload = {
        "locationId": location_id,
        "name": name,
        "redirectTo": redirect_to
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=request_headers, json=payload)
        
        if response.status_code != 201:
            logging.error(f"Failed to create trigger link: {response.text}")
            response.raise_for_status()
            
        return response.json()