from typing import Dict, Any, List
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def add_tags_to_contact(
    contact_id: str,
    tags: List[str],
    headers: Dict[str, str]
) -> Dict[str, Any]:
    """
    Add tags to a contact in Go High Level.
    
    Args:
        contact_id: The ID of the contact to add tags to
        tags: List of tag strings to add to the contact
        headers: Dictionary containing Authorization and Version headers
        
    Returns:
        Dictionary containing the added tags
    """
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
        "tags": tags
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{API_BASE_URL}/contacts/{contact_id}/tags",
                json=payload,
                headers=request_headers
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error adding tags to contact {contact_id}: {e.response.status_code} {e.response.text}")
        raise
    except Exception as e:
        logging.error(f"Error adding tags to contact {contact_id}: {str(e)}")
        raise