from typing import Dict
from ...client import get_client

def create_secret(name: str, value: str) -> Dict:
    """
    Creates a new secret.

    Args:
        name (str): The name of the secret.
        value (str): The value of the secret.

    Returns:
        Dict: The response from the API.
    """
    client = get_client()
    return client.conversational_ai.create_secret(name=name, value=value)
