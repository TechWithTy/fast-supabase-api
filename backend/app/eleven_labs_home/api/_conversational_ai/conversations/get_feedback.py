from typing import Dict
from ...client import get_client

def post_conversation_feedback(conversation_id: str, feedback: str) -> Dict:
    """
    Posts feedback for a conversation.

    Args:
        conversation_id (str): The ID of the conversation.
        feedback (str): The feedback to post (e.g., 'like').

    Returns:
        Dict: The response from the API.
    """
    client = get_client()
    return client.conversational_ai.post_conversation_feedback(
        conversation_id=conversation_id,
        feedback=feedback,
    )
