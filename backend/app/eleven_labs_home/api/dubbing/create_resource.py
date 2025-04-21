from ..client import get_client


def get_dubbing_resource(api_key: str, dubbing_id: str):
    client = get_client()

    response = client.dubbing.get_resource(dubbing_id=dubbing_id)

    return response
