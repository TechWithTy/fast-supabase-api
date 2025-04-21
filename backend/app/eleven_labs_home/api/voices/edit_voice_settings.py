from ..client import get_client


def edit_voice_settings(
    api_key, voice_id, stability, similarity_boost, style, use_speaker_boost, speed
):
    client = get_client()

    response = client.voices.edit_settings(
        voice_id=voice_id,
        stability=stability,
        similarity_boost=similarity_boost,
        style=style,
        use_speaker_boost=use_speaker_boost,
        speed=speed,
    )

    return response
