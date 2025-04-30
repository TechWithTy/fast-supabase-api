from typing import Optional
from ..client import get_client


def list_calls() -> Optional[dict]:
    """
    List all calls using the Vapi SDK.

    Returns:
        Optional[dict]: The response from the API if successful, None otherwise.
    """
    try:
        client = get_client()
        return client.calls.list()
    except Exception as e:
        print(f"Error listing calls: {e}")
        return None
