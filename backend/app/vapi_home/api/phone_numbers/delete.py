from vapi import Vapi
from typing import Optional
from ..client import get_client


def delete_phone_number(phone_number_id: str) -> Optional[dict]:
    """
    Delete a phone number using the Vapi SDK.

    Args:
        phone_number_id (str): The ID of the phone number to delete.

    Returns:
        Optional[dict]: The response from the API if successful, None otherwise.
    """
    try:
        client = get_client()
        return client.phone_numbers.delete(id=phone_number_id)
    except Exception as e:
        print(f"Error deleting phone number: {e}")
        return None

# Example usage:
client = Vapi(
    token="YOUR_TOKEN",
)
delete_phone_number("id")
