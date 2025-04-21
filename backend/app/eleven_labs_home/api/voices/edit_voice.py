from ..client import get_client


def edit_voice(api_key, voice_id, name):
    client = get_client()

    response = client.voices.edit(voice_id=voice_id, name=name)

    return response
