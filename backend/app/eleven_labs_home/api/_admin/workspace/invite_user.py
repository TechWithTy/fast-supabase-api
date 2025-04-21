from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.workspace.invite_user(
    email="john.doe@testmail.com",
)
