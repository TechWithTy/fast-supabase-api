from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.usage.get_characters_usage_metrics(
    start_unix=1,
    end_unix=1,
)
