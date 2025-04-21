from ...client import get_client

def get_generated_items():
    client = get_client()

    response = client.history.get()

    return response