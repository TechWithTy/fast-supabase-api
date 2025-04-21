from typing import List, Dict
from ...client import get_client

def list_pronunciation_dictionaries() -> List[Dict]:
    """
    Lists all pronunciation dictionaries.

    Returns:
        List[Dict]: The list of pronunciation dictionaries.
    """
    client = get_client()
    return client.pronunciation_dictionary.get_all()
