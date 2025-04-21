from typing import Optional
from ..client import get_client


def create_call() -> Optional[dict]:
    """
    Create a new call using the Vapi SDK.

    Returns:
        Optional[dict]: The response from the API if successful, None otherwise.
    """
    try:
        client = get_client()
        return client.calls.create()
    except Exception as e:
        print(f"Error creating call: {e}")
        return None
