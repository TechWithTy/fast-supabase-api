from ..client import get_client


def delete_dubbing(api_key: str, dubbing_id: str):
    client = get_client()

    response = client.dubbing.delete(dubbing_id=dubbing_id)

    return response
