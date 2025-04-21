from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.workspace.add_member_to_user_group(
    group_id="group_id",
    email="email",
)
