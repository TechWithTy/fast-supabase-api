from ..client import get_client


def get_default_voice_settings(api_key: str):
    client = get_client()
    response = client.voices.get_default_voice_settings()
    return response
