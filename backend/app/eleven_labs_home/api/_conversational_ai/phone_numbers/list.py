from typing import List, Dict
from ...client import get_client

def list_phone_numbers() -> List[Dict]:
    """
    Lists all phone numbers.

    Returns:
        List[Dict]: The list of phone numbers.
    """
    client = get_client()
    return client.conversational_ai.list_phone_numbers()
