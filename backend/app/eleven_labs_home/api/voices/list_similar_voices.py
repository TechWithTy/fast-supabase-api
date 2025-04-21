from ..client import get_client


def list_similar_voices( audio_file_path):
    client = get_client()

    with open(audio_file_path, "rb") as audio_file:
        response = client.voices.get_similar_voices(audio_file)

    return response
