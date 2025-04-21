from ..client import get_client


def get_dubbing(api_key: str, dubbing_id: str):
    client = get_client()

    response = client.dubbing.get(dubbing_id=dubbing_id)

    return response
