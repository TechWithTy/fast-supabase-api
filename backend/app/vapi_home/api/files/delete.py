from vapi import Vapi
from typing import Optional
from ..client import get_client


def delete_file(file_id: str) -> Optional[dict]:
    """
    Delete a file using the Vapi SDK.

    Args:
        file_id (str): The ID of the file to delete.

    Returns:
        Optional[dict]: The response from the API if successful, None otherwise.
    """
    try:
        client = get_client()
        return client.files.delete(id=file_id)
    except Exception as e:
        print(f"Error deleting file: {e}")
        return None

# # Example usage:
# client = Vapi(
#     token="YOUR_TOKEN",
# )
# delete_file("id")
