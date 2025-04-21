from ..client import get_client


def create_forced_alignment(api_key: str, audio_file: str, text: str):
    client = get_client()

    with open(audio_file, "rb") as audio:
        response = client.forced_alignment.create(audio=audio, text=text)

    return response
