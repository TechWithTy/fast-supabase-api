from vapi import Vapi
from typing import Optional
from ..client import get_client


def upload_file(file_path: str) -> Optional[dict]:
    """
    Upload a file using the Vapi SDK.

    Args:
        file_path (str): The path to the file to upload.

    Returns:
        Optional[dict]: The response from the API if successful, None otherwise.
    """
    try:
        client = get_client()
        with open(file_path, 'rb') as file:
            return client.files.create(file=file)
    except Exception as e:
        print(f"Error uploading file: {e}")
        return None
