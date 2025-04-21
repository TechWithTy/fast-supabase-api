from ...client import get_client

def get_history_item(history_item_id: str):
    client = get_client()

    return client.history.get(history_item_id=history_item_id)