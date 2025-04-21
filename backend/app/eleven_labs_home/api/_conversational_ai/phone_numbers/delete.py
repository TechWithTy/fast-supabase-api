from typing import Dict
from ...client import get_client

def delete_phone_number(phone_number_id: str) -> Dict:
    """
    Deletes a phone number.

    Args:
        phone_number_id (str): The ID of the phone number to delete.

    Returns:
        Dict: The response from the API.
    """
    client = get_client()
    return client.conversational_ai.delete_phone_number(phone_number_id=phone_number_id)
