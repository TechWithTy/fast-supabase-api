from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.workspace.unshare_workspace_resource(
    resource_id="resource_id",
    resource_type="voice",
)
