from typing import Optional, List
from ..client import get_client

def list_tools() -> Optional[List[dict]]:
    """
    List tools using the Vapi SDK.

    Returns:
        Optional[List[dict]]: The response from the API if successful, None otherwise.
    """
    try:
        client = get_client()
        return client.tools.list()
    except Exception as e:
        print(f"Error listing tools: {e}")
        return None
