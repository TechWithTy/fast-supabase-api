from typing import Dict, Any, List, Optional
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def update_contacts_tags(
    operation_type: str,
    contacts: List[str],
    tags: List[str],
    location_id: str,
    headers: Dict[str, str],
    remove_all_tags: bool = False
) -> Dict[str, Any]:
    """
    Update tags for multiple contacts at once.
    
    Args:
        operation_type: Type of operation ('add' or 'remove')
        contacts: List of contact IDs to process (max 500)
        tags: List of tags to add or remove (max 50)
        location_id: Location ID where the bulk request is executed
        headers: Dictionary containing Authorization and Version headers
        remove_all_tags: Option to remove all tags (only for 'remove' operation)
        
    Returns:
        Dictionary containing operation results
        
    Raises:
        ValueError: If invalid operation type is provided
        Exception: If API request fails or if required headers are missing
    """
    if operation_type not in ["add", "remove"]:
        raise ValueError("Operation type must be either 'add' or 'remove'")
    
    if remove_all_tags and operation_type != "remove":
        raise ValueError("remove_all_tags can only be used with 'remove' operation type")
    
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
        "contacts": contacts,
        "tags": tags,
        "locationId": location_id
    }
    
    if operation_type == "remove" and remove_all_tags:
        payload["removeAllTags"] = True
    
    logging.info(f"Making bulk request to {operation_type} tags for {len(contacts)} contacts")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{API_BASE_URL}/contacts/bulk/tags/update/{operation_type}",
                headers=request_headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logging.error(f"Error updating tags for contacts: {str(e)}")
        raise
