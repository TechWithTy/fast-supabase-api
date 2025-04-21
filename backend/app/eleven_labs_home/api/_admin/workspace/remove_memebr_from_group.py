from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.workspace.delete_member_from_user_group(
    group_id="group_id",
    email="email",
)
