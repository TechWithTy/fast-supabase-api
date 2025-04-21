from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.workspace.search_user_groups(
    name="name",
)
