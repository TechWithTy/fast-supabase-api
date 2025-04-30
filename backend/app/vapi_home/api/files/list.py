from typing import Optional, List
from ..client import get_client

def list_files() -> Optional[List[dict]]:
    """
    List files using the Vapi SDK.

    Returns:
        Optional[List[dict]]: The response from the API if successful, None otherwise.
    """
    try:
        client = get_client()
        return client.files.list()
    except Exception as e:
        print(f"Error listing files: {e}")
        return None
