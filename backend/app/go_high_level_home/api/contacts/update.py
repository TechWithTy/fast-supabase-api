from typing import Dict, Any, List, Optional
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

class DndSetting:
    status: str
    message: str
    code: str

class UpdateCustomField:
    id: Optional[str]
    key: Optional[str]
    field_value: str

async def update_contact(
    contact_id: str,
    update_data: Dict[str, Any],
    headers: Dict[str, str]
) -> Dict[str, Any]:
    """
    Update a contact in the Go High Level API.
    
    Args:
        contact_id: The ID of the contact to update
        update_data: Dictionary containing the contact data to update
        headers: Dictionary containing Authorization and Version headers
        
    Returns:
        Dictionary containing updated contact data
        
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
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    logging.info(f"Making request to update contact: {contact_id}")
    
    try:
        # Make the API request to update contact
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.put(
                f"{API_BASE_URL}/contacts/{contact_id}",
                headers=request_headers,
                json=update_data
            )
            
        # Handle the API response
        if response.status_code != 200:
            error_detail = response.text
            logging.error(f"API request failed with status {response.status_code}: {error_detail}")
            raise Exception(f"API request failed with status {response.status_code}: {error_detail}")
            
        return response.json()
    
    except Exception as e:
        logging.error(f"Error updating contact: {str(e)}")
        raise