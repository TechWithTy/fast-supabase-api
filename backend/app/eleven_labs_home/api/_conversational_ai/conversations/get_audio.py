from typing import Dict
from ...client import get_client

def get_conversation_audio(conversation_id: str) -> Dict:
    """
    Retrieves audio for a conversation.

    Args:
        conversation_id (str): The ID of the conversation.

    Returns:
        Dict: The response from the API.
    """
    client = get_client()
    return client.conversational_ai.get_conversation_audio(conversation_id=conversation_id)