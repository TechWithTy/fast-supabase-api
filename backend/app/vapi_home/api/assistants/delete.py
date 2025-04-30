from typing import Optional
from ..client import get_client


def delete_assistant(assistant_id: str) -> Optional[dict]:
    """
    Delete an assistant using the Vapi SDK.

    Args:
        assistant_id (str): The ID of the assistant to delete.

    Returns:
        Optional[dict]: The response from the API if successful, None otherwise.
    """
    try:
        client = get_client()
        return client.assistants.delete(id=assistant_id)
    except Exception as e:
        print(f"Error deleting assistant: {e}")
        return None

client = get_client()
response = delete_assistant("id")
