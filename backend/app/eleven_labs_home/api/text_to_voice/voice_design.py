from ..client import get_client


def create_voice_previews(api_key: str, voice_description: str):
    client = get_client()

    response = client.voice_design.create_previews(voice_description=voice_description)

    return response


# Usage example:
# api_key = "your_api_key_here"
# voice_description = "A sassy squeaky mouse"
# result = create_voice_previews(api_key, voice_description)
# print(result)
