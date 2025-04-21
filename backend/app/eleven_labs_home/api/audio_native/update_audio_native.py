from ..client import get_client
from typing import BinaryIO


def update_audio_native_project(api_key: str, project_id: str, file: BinaryIO):
    client = get_client()

    response = client.audio_native.update(project_id=project_id, file=file)

    return response
