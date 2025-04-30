from typing import Optional
from ..client import get_client


def get_assistant(assistant_id: str) -> Optional[dict]:
    """
    Get an assistant using the Vapi SDK.

    Args:
        assistant_id (str): The ID of the assistant to retrieve.

    Returns:
        Optional[dict]: The response from the API if successful, None otherwise.
    """
    try:
        client = get_client()
        return client.assistants.get(id=assistant_id)
    except Exception as e:
        print(f"Error getting assistant: {e}")
        return None
