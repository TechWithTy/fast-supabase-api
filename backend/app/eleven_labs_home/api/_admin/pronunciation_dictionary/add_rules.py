from typing import Dict
from ...client import get_client
from elevenlabs.pronunciation_dictionary import (
    PronunciationDictionaryRule_Alias,
)

def add_pronunciation_dictionary_rules(pronunciation_dictionary_id: str, rules: list) -> Dict:
    """
    Adds rules to a pronunciation dictionary.

    Args:
        pronunciation_dictionary_id (str): The ID of the dictionary.
        rules (list): The rules to add.

    Returns:
        Dict: The response from the API.
    """
    client = get_client()
    return client.pronunciation_dictionary.add_rules(
        pronunciation_dictionary_id=pronunciation_dictionary_id,
        rules=rules,
    )

# # Example usage:
# rules = [
#     PronunciationDictionaryRule_Alias(
#         string_to_replace="Thailand",
#         alias="tie-land",
#     )
# ]
# response = add_pronunciation_dictionary_rules(
#     pronunciation_dictionary_id="21m00Tcm4TlvDq8ikWAM",
#     rules=rules,
# )
