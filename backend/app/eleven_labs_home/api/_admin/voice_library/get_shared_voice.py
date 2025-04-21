from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.voices.get_shared(
    page_size=1,
    gender="female",
    language="en",
)
