from ..client import get_client


def stream_speech_with_timing(
    api_key,
    voice_id,
    text,
    model_id="eleven_multilingual_v2",
    output_format="mp3_44100_128",
):
    client = get_client()

    audio = client.generate(
        text=text,
        voice=voice_id,
        model=model_id,
        stream=True,
        output_format=output_format,
    )

    for chunk in audio:
        yield chunk


# Usage example:
# api_key = "your_api_key_here"
# voice_id = "JBFqnCBsd6RMkjVDRZzb"
# text = "The first move is what sets everything in motion."
# for audio_chunk in stream_speech_with_timing(api_key, voice_id, text):
#     # Process or play the audio chunk
#     pass
