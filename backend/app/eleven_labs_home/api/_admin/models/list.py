from ...client import get_client

def list_models():
    client = get_client()

    return client.models.get_all()