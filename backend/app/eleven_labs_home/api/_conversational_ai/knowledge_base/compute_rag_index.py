from typing import Dict
from ...client import get_client

def compute_rag_index(documentation_id: str) -> Dict:
    """
    Computes the RAG index for a knowledge base document.

    Args:
        documentation_id (str): The ID of the document.

    Returns:
        Dict: The response from the API.
    """
    client = get_client()
    return client.conversational_ai.compute_rag_index(documentation_id=documentation_id)

# Example usage:
# client = get_client()
# client.conversational_ai.rag_index_status(
#     documentation_id="21m00Tcm4TlvDq8ikWAM",
#     model="e5_mistral_7b_instruct",
# )
