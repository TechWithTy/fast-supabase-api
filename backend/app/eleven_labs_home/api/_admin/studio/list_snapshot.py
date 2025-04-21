from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.studio.projects.get_snapshots(
    project_id="21m00Tcm4TlvDq8ikWAM",
)
