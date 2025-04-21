from ..client import get_client


def dub_segments(api_key: str, dubbing_id: str, segments: list):
    client = get_client()

    response = client.dubbing.dub(dubbing_id=dubbing_id, segments=segments)

    return response
