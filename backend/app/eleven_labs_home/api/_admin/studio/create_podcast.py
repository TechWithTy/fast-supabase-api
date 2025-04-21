from typing import Dict
from ...client import get_client
from elevenlabs import PodcastConversationModeData, PodcastTextSource
from elevenlabs.studio import BodyCreatePodcastV1StudioPodcastsPostMode_Conversation


def create_podcast(model_id: str, host_voice_id: str, guest_voice_id: str, text: str) -> Dict:
    """
    Create a new podcast.

    Args:
        model_id: The ID of the model to use.
        host_voice_id: The ID of the host's voice.
        guest_voice_id: The ID of the guest's voice.
        text: The text content of the podcast.

    Returns:
        A dictionary containing the podcast details.
    """
    client = get_client()
    
    return client.studio.create_podcast(
        model_id=model_id,
        mode=BodyCreatePodcastV1StudioPodcastsPostMode_Conversation(
            conversation=PodcastConversationModeData(
                host_voice_id=host_voice_id,
                guest_voice_id=guest_voice_id,
            ),
        ),
        source=PodcastTextSource(
            text=text,
        ),
    )
