from typing import Optional
from ..client import get_client

def update_assistant(assistant_id: str, update_data: dict) -> Optional[dict]:
    """
    Update an assistant using the Vapi SDK.

    Args:
        assistant_id (str): The ID of the assistant to update.
        update_data (dict): The data to update the assistant with.

    Returns:
        Optional[dict]: The response from the API if successful, None otherwise.
    """
    try:
        client = get_client()
        return client.assistants.update(id=assistant_id, **update_data)
    except Exception as e:
        print(f"Error updating assistant: {e}")
        return None
