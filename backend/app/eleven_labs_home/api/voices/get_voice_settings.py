from ..client import get_client


def get_voice_settings(api_key: str, voice_id: str):
    client = get_client()
    response = client.voices.get_settings(voice_id=voice_id)
    return response
