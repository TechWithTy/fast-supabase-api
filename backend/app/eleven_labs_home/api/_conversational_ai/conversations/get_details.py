from typing import Dict
from ...client import get_client

def get_conversation_details(conversation_id: str) -> Dict:
    """
    Retrieves details for a conversation.

    Args:
        conversation_id (str): The ID of the conversation.

    Returns:
        Dict: The response from the API.
    """
    client = get_client()
    return client.conversational_ai.get_conversation_details(conversation_id=conversation_id)
