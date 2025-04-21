from typing import Dict
from ...client import get_client

def get_knowledge_base_document_content(documentation_id: str) -> Dict:
    """
    Retrieves the content of a knowledge base document.

    Args:
        documentation_id (str): The ID of the document.

    Returns:
        Dict: The response from the API.
    """
    client = get_client()
    return client.conversational_ai.get_knowledge_base_document_content(documentation_id=documentation_id)
