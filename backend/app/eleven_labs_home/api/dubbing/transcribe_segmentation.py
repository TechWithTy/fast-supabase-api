from ..client import get_client


def transcribe_segments(api_key: str, dubbing_id: str, segments: list):
    client = get_client()

    response = client.dubbing.transcribe(dubbing_id=dubbing_id, segments=segments)

    return response
