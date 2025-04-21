from ..client import get_client


def stream_speech(
    api_key,
    voice_id,
    text,
    model_id="eleven_multilingual_v2",
    output_format="mp3_44100_128",
):
    # Initialize the ElevenLabs client
    client = get_client()

    # Generate the audio stream
    audio_stream = client.generate(
        text=text, voice=voice_id, model=model_id, stream=True
    )

    # Stream the audio
    for chunk in audio_stream:
        if chunk:
            yield chunk


# Usage example:
# for audio_chunk in stream_speech("your_api_key", "JBFqnCBsd6RMkjVDRZzb", "The first move is what sets everything in motion."):
#     # Process or play the audio chunk
#     pass
