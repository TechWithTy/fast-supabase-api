from vapi import Vapi
from typing import Optional
from ..client import get_client


def update_file(file_id: str, update_data: dict) -> Optional[dict]:
    """
    Update a file using the Vapi SDK.

    Args:
        file_id (str): The ID of the file to update.
        update_data (dict): The update configuration.

    Returns:
        Optional[dict]: The response from the API if successful, None otherwise.
    """
    try:
        client = get_client()
        return client.files.update(id=file_id, **update_data)
    except Exception as e:
        print(f"Error updating file: {e}")
        return None

# # Example usage:
# client = Vapi(
#     token="YOUR_TOKEN",
# )
# update_file(
#     file_id="id",
#     update_data={}
# )
