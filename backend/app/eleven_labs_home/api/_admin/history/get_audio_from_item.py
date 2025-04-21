from ...client import get_client

def get_audio_from_history_item(history_item_id: str):
    client = get_client()
    response = client.history.download(history_item_ids=[history_item_id])
    return response