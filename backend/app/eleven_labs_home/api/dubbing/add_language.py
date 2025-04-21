from ..client import get_client


def add_language_to_dubbing_resource(
    api_key: str, dubbing_id: str, language_data: dict
):
    client = get_client()

    response = client.dubbing.add_language(dubbing_id=dubbing_id, json=language_data)

    return response
