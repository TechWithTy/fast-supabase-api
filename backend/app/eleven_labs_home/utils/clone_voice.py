from typing import BinaryIO
from ..api.client import get_client
from .get_voice_data import get_customer_voice_data


def use_customer_voice(customer_id: str, text: str) -> BinaryIO:
    """
    Use a customer's voice for text generation.

    Args:
        customer_id: The unique ID of the customer
        text: The text to generate speech from

    Returns:
        The audio stream of generated speech

    Raises:
        Exception: If speech generation fails
    """
    # Get customer-specific data to ensure isolation
    customer_data = get_customer_voice_data(customer_id)
    voice_name = customer_data.get("voiceName")

    try:
        client = get_client()
        voices = client.voices.get_all()
        voice = next((v for v in voices if v.name == voice_name), None)
        if not voice:
            raise Exception(f"Voice '{voice_name}' not found")

        audio_stream = client.generate(
            text=text, voice=voice.voice_id, model_id="eleven_multilingual_v2"
        )
        return audio_stream
    except Exception as error:
        print(f"Error generating speech: {error}")
        raise Exception("Speech generation failed.")
