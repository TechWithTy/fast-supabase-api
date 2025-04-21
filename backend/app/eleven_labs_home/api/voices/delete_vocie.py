from ..client import get_client


def delete_voice(api_key: str, voice_id: str):
    client = get_client()
    response = client.voices.delete(voice_id)
    return response
