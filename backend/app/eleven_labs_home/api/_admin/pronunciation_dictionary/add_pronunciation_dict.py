from typing import Dict
from ...client import get_client
from elevenlabs.pronunciation_dictionary import (
    BodyAddAPronunciationDictionaryV1PronunciationDictionariesAddFromRulesPostRulesItem_Alias,
)

def add_pronunciation_dictionary(name: str, rules: list) -> Dict:
    """
    Adds a pronunciation dictionary from rules.

    Args:
        name (str): The name of the dictionary.
        rules (list): The rules to add to the dictionary.

    Returns:
        Dict: The response from the API.
    """
    client = get_client()
    return client.pronunciation_dictionary.add_from_rules(name=name, rules=rules)

# # Example usage:
# rules = [
#     BodyAddAPronunciationDictionaryV1PronunciationDictionariesAddFromRulesPostRulesItem_Alias(
#         string_to_replace="Thailand",
#         alias="tie-land",
#     )
# ]
# response = add_pronunciation_dictionary(name="My Dictionary", rules=rules)
