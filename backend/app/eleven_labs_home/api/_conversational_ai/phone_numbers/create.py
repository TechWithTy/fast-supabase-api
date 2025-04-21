from typing import Dict
from ...client import get_client

def create_phone_number(phone_number: str) -> Dict:
    """
    Creates a new phone number.

    Args:
        phone_number (str): The phone number to create.

    Returns:
        Dict: The response from the API.
    """
    client = get_client()
    return client.conversational_ai.create_phone_number(phone_number=phone_number)
