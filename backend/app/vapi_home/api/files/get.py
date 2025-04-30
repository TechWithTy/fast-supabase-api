from vapi import Vapi
from typing import Optional
from ..client import get_client


def get_file(file_id: str) -> Optional[dict]:
    """
    Get a file using the Vapi SDK.

    Args:
        file_id (str): The ID of the file to retrieve.

    Returns:
        Optional[dict]: The response from the API if successful, None otherwise.
    """
    try:
        client = get_client()
        return client.files.get(id=file_id)
    except Exception as e:
        print(f"Error getting file: {e}")
        return None

# # Example usage:
# file_id = "id"
# file = get_file(file_id)
