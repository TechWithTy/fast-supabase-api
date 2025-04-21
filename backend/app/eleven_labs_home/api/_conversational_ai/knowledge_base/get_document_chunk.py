from typing import Dict
from ...client import get_client

def get_knowledge_base_document_part_by_id(documentation_id: str, chunk_id: str) -> Dict:
    """
    Retrieves a specific chunk of a knowledge base document.

    Args:
        documentation_id (str): The ID of the document.
        chunk_id (str): The ID of the chunk to retrieve.

    Returns:
        Dict: The response from the API.
    """
    client = get_client()
    return client.conversational_ai.get_knowledge_base_document_part_by_id(
        documentation_id=documentation_id,
        chunk_id=chunk_id,
    )
