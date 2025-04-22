from ..client import get_client


def get_call(call_id: str) -> dict | None:
    """
    Get a call using the Vapi SDK.

    Args:
        call_id (str): The ID of the call to retrieve.

    Returns:
        Optional[dict]: The response from the API if successful, None otherwise.
    """
    try:
        client = get_client()
        return client.calls.get(id=call_id)
    except Exception as e:
        print(f"Error getting call: {e}")
        return None
