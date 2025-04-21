from ..client import get_client


def get_dubbed_transcript(api_key: str, dubbing_id: str, language_code: str):
    client = get_client()

    response = client.dubbing.get_transcript(
        dubbing_id=dubbing_id, language_code=language_code
    )

    return response
