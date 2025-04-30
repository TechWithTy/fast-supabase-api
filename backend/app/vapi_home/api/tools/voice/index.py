from typing import List, Dict, Any
from . import get_client

def sync_voice_with_vapi(customer_id: str, voice_id: str) -> None:
    """
    Sync a cloned voice with VAPI.

    Args:
        customer_id (str): The unique ID of the customer.
        voice_id (str): The cloned voice ID from ElevenLabs.

    Raises:
        Exception: If the sync operation fails.
    """
    try:
        client = get_client()
        client.sync_voice(customer_id, voice_id)
        print(f"Voice ID {voice_id} synced successfully for customer {customer_id}")
    except Exception as error:
        print(f"Error syncing voice with VAPI: {error}")
        raise Exception("Sync with VAPI failed.") from error

def fetch_customer_voices(customer_id: str) -> List[Dict[str, Any]]:
    """
    Fetch all cloned voices for a specific customer from VAPI.

    Args:
        customer_id (str): The unique ID of the customer.

    Returns:
        List[Dict[str, Any]]: A list of voices for the customer.

    Raises:
        Exception: If fetching voices fails.
    """
    try:
        client = get_client()
        voices = client.get_customer_voices(customer_id)
        print(f"Fetched {len(voices)} voices for customer {customer_id}")
        return voices
    except Exception as error:
        print(f"Error fetching customer voices from VAPI: {error}")
        raise Exception("Fetch customer voices failed.") from error
