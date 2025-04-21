from ..client import get_client


def create_speech(
    api_key: str,
    voice_id: str,
    text: str,
    model_id: str = "eleven_multilingual_v2",
    output_format: str = "mp3_44100_128",
    **kwargs,
):
    client = get_client()

    audio = client.generate(
        text=text, voice=voice_id, model=model_id, output_format=output_format, **kwargs
    )

    return audio


# Usage example:
# api_key = "your_api_key_here"
# voice_id = "JBFqnCBsd6RMkjVDRZzb"
# text = "The first move is what sets everything in motion."
# audio = create_speech(api_key, voice_id, text)
