from ..client import get_client


def delete_call(call_id: str) -> dict | None:
    """
    Delete a call using the Vapi SDK.

    Args:
        call_id (str): The ID of the call to delete.

    Returns:
        Optional[dict]: The response from the API if successful, None otherwise.
    """
    try:
        client = get_client()
        return client.calls.delete(id=call_id)
    except Exception as e:
        print(f"Error deleting call: {e}")
        return None

