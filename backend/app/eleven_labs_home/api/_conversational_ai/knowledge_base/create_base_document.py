from typing import Dict
from ...client import get_client

def create_knowledge_base_document(documentation_id: str) -> Dict:
    """
    Creates a new knowledge base document.

    Args:
        documentation_id (str): The ID of the document.

    Returns:
        Dict: The response from the API.
    """
    client = get_client()
    return client.conversational_ai.create_knowledge_base_document(documentation_id=documentation_id)
