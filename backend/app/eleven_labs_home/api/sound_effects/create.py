from ..client import get_client


def create_sound_effect(api_key: str, text: str):
    client = get_client()

    response = client.sound_generation.generate(text=text)

    return response


# Usage example:
# api_key = "your_api_key_here"
# text = "Spacious braam suitable for high-impact movie trailer moments"
# sound_effect = create_sound_effect(api_key, text)
