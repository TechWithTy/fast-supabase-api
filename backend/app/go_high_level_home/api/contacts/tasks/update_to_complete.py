from typing import Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def update_task_to_complete(
    contact_id: str,
    task_id: str,
    headers: Dict[str, str],
    completed: bool = True
) -> Dict[str, Any]:
    """
    Update a task's completed status for a contact in Go High Level.
    
    Args:
        contact_id: ID of the contact
        task_id: ID of the task to update
        headers: Dictionary containing Authorization and Version headers
        completed: Whether the task is completed (defaults to True)
        
    Returns:
        Dict containing the updated task data
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
        "completed": completed
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{API_BASE_URL}/contacts/{contact_id}/tasks/{task_id}/completed",
                json=payload,
                headers=request_headers
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {e}")
        raise
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise