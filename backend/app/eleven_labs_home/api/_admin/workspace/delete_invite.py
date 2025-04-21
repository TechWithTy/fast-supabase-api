from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.workspace.delete_existing_invitation(
    email="john.doe@testmail.com",
)
