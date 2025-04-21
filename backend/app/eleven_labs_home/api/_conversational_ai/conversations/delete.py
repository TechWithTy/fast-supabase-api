from elevenlabs import ElevenLabs

def delete_conversation(conversation_id: str) -> None:
    """
    Deletes a conversation by its ID.

    Args:
        conversation_id (str): The ID of the conversation to delete.
    """
    client = ElevenLabs(
        api_key="YOUR_API_KEY",
    )
    client.conversational_ai.delete_conversation(conversation_id=conversation_id)

delete_conversation(conversation_id="21m00Tcm4TlvDq8ikWAM")
