from typing import Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def create_task(
    contact_id: str,
    headers: Dict[str, str],
    title: str,
    due_date: str,
    completed: bool,
    body: str = None,
    assigned_to: str = None
) -> Dict[str, Any]:
    """
    Create a task for a contact in Go High Level.
    
    Args:
        contact_id: ID of the contact
        headers: Dictionary containing Authorization and Version headers
        title: Title of the task
        due_date: Due date in ISO format (e.g. "2020-10-25T11:00:00Z")
        completed: Whether the task is completed
        body: Optional body/description of the task
        assigned_to: Optional ID of user assigned to the task
        
    Returns:
        Dict containing the created task data
    """
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    if not headers.get("Version"):
        headers["Version"] = API_VERSION

    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers["Version"],
        "Content-Type": "application/json"
    }
    
    payload = {
        "title": title,
        "dueDate": due_date,
        "completed": completed
    }
    
    if body:
        payload["body"] = body
    
    if assigned_to:
        payload["assignedTo"] = assigned_to
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{API_BASE_URL}/contacts/{contact_id}/tasks",
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