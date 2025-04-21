from ...client import get_client
def delete_history_item(history_item_id: str):
    client = get_client()
    response = client.history.delete(history_item_id=history_item_id)
    return response