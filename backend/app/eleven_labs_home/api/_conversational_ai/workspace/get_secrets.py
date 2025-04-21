from typing import List, Dict
from ...client import get_client

def get_secrets() -> List[Dict]:
    """
    Retrieves all secrets.

    Returns:
        List[Dict]: The list of secrets.
    """
    client = get_client()
    return client.conversational_ai.get_secrets()
