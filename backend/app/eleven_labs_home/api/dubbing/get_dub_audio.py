from ..client import get_client


def get_dubbed_audio(api_key: str, dubbing_id: str, language_code: str):
    client = get_client()

    response = client.dubbing.get_audio(
        dubbing_id=dubbing_id, language_code=language_code
    )

    return response
