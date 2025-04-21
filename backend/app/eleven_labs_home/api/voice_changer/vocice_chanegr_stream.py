from ..client import get_client


def voice_changer_stream(
    api_key,
    voice_id,
    audio_file,
    model_id="eleven_multilingual_sts_v2",
    output_format="mp3_44100_128",
):
    client = get_client()

    with open(audio_file, "rb") as audio:
        response = client.speech_to_speech(
            voice_id=voice_id,
            audio=audio,
            model_id=model_id,
            output_format=output_format,
            stream=True,
        )

    for chunk in response:
        yield chunk


# Usage example:
# api_key = "your_api_key_here"
# voice_id = "JBFqnCBsd6RMkjVDRZzb"
# audio_file = "path/to/your/audio/file.mp3"
# for audio_chunk in voice_changer_stream(api_key, voice_id, audio_file):
#     # Process or play the audio chunk
#     pass
