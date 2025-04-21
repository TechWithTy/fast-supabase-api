from ..client import get_client


def get_audio_native_project_settings(api_key: str, project_id: str):
    client = get_client()

    response = client.audio_native.get_settings(project_id=project_id)

    return response
