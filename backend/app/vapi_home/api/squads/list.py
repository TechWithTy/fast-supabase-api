from typing import Optional, List
from ..client import get_client

def list_squads() -> Optional[List[dict]]:
    """
    List squads using the Vapi SDK.

    Returns:
        Optional[List[dict]]: The response from the API if successful, None otherwise.
    """
    try:
        client = get_client()
        return client.squads.list()
    except Exception as e:
        print(f"Error listing squads: {e}")
        return None
