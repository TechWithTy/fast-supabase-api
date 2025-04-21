from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.workspace.update_member(
    email="email",
)
