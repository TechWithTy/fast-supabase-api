from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.workspace.share_workspace_resource(
    resource_id="resource_id",
    role="admin",
    resource_type="voice",
)
