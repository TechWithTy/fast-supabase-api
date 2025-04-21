from typing import Dict, Any, Optional
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def update_task(
    contact_id: str,
    task_id: str,
    headers: Dict[str, str],
    title: Optional[str] = None,
    body: Optional[str] = None,
    due_date: Optional[str] = None,
    completed: Optional[bool] = None,
    assigned_to: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update a task for a contact in Go High Level.
    
    Args:
        contact_id: ID of the contact
        task_id: ID of the task to update
        headers: Dictionary containing request headers
        title: Optional new title of the task
        body: Optional new body/description of the task
        due_date: Optional new due date in ISO format (e.g. "2020-10-25T11:00:00Z")
        completed: Optional new completed status
        assigned_to: Optional new ID of user assigned to the task
        
    Returns:
        Dict containing the updated task data
    """
    if "Authorization" not in headers or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    if "Version" not in headers:
        headers["Version"] = API_VERSION

    headers["Content-Type"] = "application/json"
    
    payload = {}
    if title is not None:
        payload["title"] = title
    if body is not None:
        payload["body"] = body
    if due_date is not None:
        payload["dueDate"] = due_date
    if completed is not None:
        payload["completed"] = completed
    if assigned_to is not None:
        payload["assignedTo"] = assigned_to
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{API_BASE_URL}/contacts/{contact_id}/tasks/{task_id}",
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"Error updating task: {str(e)}")
        raise