from typing import Dict
from ...client import get_client

def get_pronunciation_dictionary(pronunciation_dictionary_id: str) -> Dict:
    """
    Retrieves a pronunciation dictionary by ID.

    Args:
        pronunciation_dictionary_id (str): The ID of the dictionary.

    Returns:
        Dict: The response from the API.
    """
    client = get_client()
    return client.pronunciation_dictionary.get(pronunciation_dictionary_id=pronunciation_dictionary_id)
