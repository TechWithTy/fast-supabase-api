from ..client import get_client
from typing import BinaryIO


def create_transcript(
    api_key: str, file: BinaryIO, model_id: str = "eleven_multilingual_v2"
) -> str:
    client = get_client()

    response = client.speech_to_text.convert(audio=file, model_id=model_id)

    return response.text
