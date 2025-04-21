from typing import Dict, Any, List
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def add_followers(
    contact_id: str,
    followers: List[str],
    headers: Dict[str, str]
) -> Dict[str, Any]:
    """
    Add followers to a contact in Go High Level.
    
    Args:
        contact_id: The ID of the contact to add followers to
        followers: List of follower IDs to add to the contact
        headers: Dictionary containing request headers
        
    Returns:
        Dictionary containing the response data with followers and followersAdded
    """
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers.get("Version", API_VERSION),
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    payload = {
        "followers": followers
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{API_BASE_URL}/contacts/{contact_id}/followers",
                json=payload,
                headers=request_headers
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error adding followers to contact {contact_id}: {e.response.status_code} {e.response.text}")
        raise
    except Exception as e:
        logging.error(f"Error adding followers to contact {contact_id}: {str(e)}")
        raise