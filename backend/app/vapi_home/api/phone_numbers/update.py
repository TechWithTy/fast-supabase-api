from vapi import Vapi
from typing import Optional
from ..client import get_client


def update_phone_number(phone_number_id: str, update_data: dict) -> Optional[dict]:
    """
    Update a phone number using the Vapi SDK.

    Args:
        phone_number_id (str): The ID of the phone number to update.
        update_data (dict): The update configuration.

    Returns:
        Optional[dict]: The response from the API if successful, None otherwise.
    """
    try:
        client = get_client()
        return client.phone_numbers.update(id=phone_number_id, **update_data)
    except Exception as e:
        print(f"Error updating phone number: {e}")
        return None

# Example usage:
client = Vapi(
    token="YOUR_TOKEN",
)
update_phone_number(
    phone_number_id="id",
    update_data={},
)
