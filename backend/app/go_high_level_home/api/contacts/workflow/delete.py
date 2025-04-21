from typing import Dict, Any, Optional
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def delete_contact_from_workflow(
    contact_id: str,
    workflow_id: str,
    headers: Dict[str, str],
    event_start_time: Optional[str] = None
) -> Dict[str, bool]:
    """
    Delete a contact from a workflow in Go High Level API.
    
    Args:
        contact_id: The ID of the contact
        workflow_id: The ID of the workflow
        headers: Dictionary containing Authorization and Version headers
        event_start_time: Optional start time for the event in ISO format (e.g. "2021-06-23T03:30:00+01:00")
        
    Returns:
        Dictionary containing success status
        
    Raises:
        Exception: If the API request fails or if required headers are missing
    """
    # Validate and extract auth token
    auth_token = headers.get("Authorization", "")
    if not auth_token.startswith("Bearer "):
        raise Exception("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")
    auth_token = auth_token.split("Bearer ")[1]

    # Set default version if not provided
    version = headers.get("Version", API_VERSION)
    
    # Prepare request headers
    request_headers = {
        "Authorization": f"Bearer {auth_token}",
        "Version": version,
        "Accept": "application/json"
    }
    
    # Prepare request body if event_start_time is provided
    request_body = {"eventStartTime": event_start_time} if event_start_time else None
    
    logging.info(f"Making request to delete contact {contact_id} from workflow {workflow_id}")
    
    try:
        # Make the API request to delete contact from workflow
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.delete(
                f"{API_BASE_URL}/contacts/{contact_id}/workflow/{workflow_id}",
                headers=request_headers,
                json=request_body
            )
            
        # Handle the API response
        if response.status_code != 200:
            error_detail = response.text
            logging.error(f"API request failed with status {response.status_code}: {error_detail}")
            raise Exception(f"API request failed with status {response.status_code}: {error_detail}")
            
        return response.json()
    except Exception as e:
        logging.error(f"Error deleting contact from workflow: {str(e)}")
        raise