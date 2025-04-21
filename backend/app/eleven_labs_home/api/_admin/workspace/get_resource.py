from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.workspace.get_resource(
    resource_id="resource_id",
    resource_type="voice",
)
