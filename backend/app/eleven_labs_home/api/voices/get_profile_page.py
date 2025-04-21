from ..client import get_client


def get_profile_page(api_key: str, handle: str):
    client = get_client()
    response = client.get(f"/profile/{handle}")
    return response.json()
