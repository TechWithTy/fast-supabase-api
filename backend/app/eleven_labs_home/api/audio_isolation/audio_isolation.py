from ..client import get_client


def audio_isolation(api_key: str, audio_file: str):
    client = get_client()

    with open(audio_file, "rb") as audio:
        response = client.audio_isolation.isolate(audio=audio)

    return response


# Usage example:
# api_key = "your_api_key_here"
# audio_file = "path/to/your/audio/file.mp3"
# result = audio_isolation(api_key, audio_file)
