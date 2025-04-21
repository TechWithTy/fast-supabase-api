from typing import Dict
from ...client import get_client

def remove_pronunciation_dictionary_rules(pronunciation_dictionary_id: str, rule_strings: list) -> Dict:
    """
    Removes rules from a pronunciation dictionary.

    Args:
        pronunciation_dictionary_id (str): The ID of the dictionary.
        rule_strings (list): The rule strings to remove.

    Returns:
        Dict: The response from the API.
    """
    client = get_client()
    return client.pronunciation_dictionary.remove_rules(
        pronunciation_dictionary_id=pronunciation_dictionary_id,
        rule_strings=rule_strings,
    )
