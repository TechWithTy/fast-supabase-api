from typing import Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def get_contact(contact_id: str, bearer_token: str) -> Dict[Any, Any]:
    """
    Get a contact by ID from the Go High Level API.
    
    Args:
        contact_id: The ID of the contact to retrieve
        bearer_token: The bearer token for API authorization
        
    Returns:
        Dict containing the contact information
    """
    url = f"{API_BASE_URL}/contacts/{contact_id}"
    
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Version": API_VERSION,
        "Accept": "application/json"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {e}")
        raise
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise