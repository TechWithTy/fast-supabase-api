from ..client import get_client


def get_voice(voice_id: str):
    client = get_client()
    voice = client.voices.get(voice_id)
    return voice
