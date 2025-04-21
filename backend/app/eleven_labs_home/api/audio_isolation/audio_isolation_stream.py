from ..client import get_client


def audio_isolation_stream(api_key, audio_file):
    client = get_client()

    with open(audio_file, "rb") as audio:
        response = client.audio_isolation.isolate(audio=audio, stream=True)

    for chunk in response:
        yield chunk
