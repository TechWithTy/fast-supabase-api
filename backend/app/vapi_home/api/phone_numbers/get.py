from typing import Optional
from ..client import get_client

def get_phone_number(phone_number_id: str) -> Optional[dict]:
    """
    Get a phone number using the Vapi SDK.

    Args:
        phone_number_id (str): The ID of the phone number to retrieve.

    Returns:
        Optional[dict]: The response from the API if successful, None otherwise.
    """
    try:
        client = get_client()
        return client.phone_numbers.get(id=phone_number_id)
    except Exception as e:
        print(f"Error getting phone number: {e}")
        return None

# Example usage:
phone_number_id = "id"
response = get_phone_number(phone_number_id)
