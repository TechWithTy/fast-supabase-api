from typing import List, Dict
from ...client import get_client

def list_knowledge_base_documents() -> List[Dict]:
    """
    Lists all knowledge base documents.

    Returns:
        List[Dict]: The list of knowledge base documents.
    """
    client = get_client()
    return client.conversational_ai.list_knowledge_base_documents()
