from typing import Dict
from ...client import get_client


def create_pronunciation_dictionary_from_file(name: str, file_path: str) -> Dict:
    """
    Creates a pronunciation dictionary from a file.

    Args:
        name (str): The name of the dictionary.
        file_path (str): The path to the file containing the dictionary rules.

    Returns:
        Dict: The response from the API.
    """
    client = get_client()
    with open(file_path, 'rb') as file:
        return client.pronunciation_dictionary.add_from_file(name=name, file=file)
