from typing import Optional
from ..client import get_client

def list_assistants() -> Optional[dict]:
    """
    List all assistants using the Vapi SDK.

    Returns:
        Optional[dict]: The response from the API if successful, None otherwise.
    """
    try:
        client = get_client()
        return client.assistants.list()
    except Exception as e:
        print(f"Error listing assistants: {e}")
        return None
