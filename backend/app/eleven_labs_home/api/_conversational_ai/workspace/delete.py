from typing import Dict
from ...client import get_client

def delete_secret(secret_id: str) -> Dict:
    """
    Deletes a secret.

    Args:
        secret_id (str): The ID of the secret to delete.

    Returns:
        Dict: The response from the API.
    """
    client = get_client()
    return client.conversational_ai.delete_secret(secret_id=secret_id)
