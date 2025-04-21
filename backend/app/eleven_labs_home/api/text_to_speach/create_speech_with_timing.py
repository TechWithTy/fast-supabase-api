from ..client import get_client
from typing import Dict, Any


def create_speech_with_timing(
    voice_id: str,
    text: str,
    api_key: str,
    model: str = "eleven_monolingual_v1",
    **kwargs,
) -> Dict[str, Any]:
    client = get_client()

    audio = client.generate(text=text, voice=voice_id, model=model, **kwargs)

    return audio.metadata
