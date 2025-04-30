import os
from typing import List, Dict, Any
from . import get_client  # Importing the method to get the API client


def sync_customer_voice_with_vapi(customer_id: str, voice_id: str) -> None:
    """Sync the cloned voice with VAPI for the given customer.

    Args:
        customer_id (str): The unique ID of the customer.
        voice_id (str): The cloned voice ID from ElevenLabs.

    Raises:
        Exception: If the sync operation fails.
    """
    try:
        # Get the VAPI client
        client = get_client()
        # Sync the cloned voice with VAPI
        client.sync_voice(customer_id, voice_id)  # Assuming sync_voice is a method in the SDK
        print(f"Successfully synced voice {voice_id} for customer {customer_id}")
    except Exception as error:
        print(f"Error syncing voice {voice_id} for customer {customer_id}: {error}")
        raise Exception("Failed to sync voice with VAPI") from error


def get_customer_voices(customer_id: str) -> List[Dict[str, Any]]:
    """Fetch only the voices for the authenticated customer from VAPI.

    Args:
        customer_id (str): The unique ID of the customer.

    Returns:
        List[Dict[str, Any]]: List of voice data for that customer.

    Raises:
        Exception: If fetching voices fails.
    """
    try:
        # Get the VAPI client
        client = get_client()
        # Fetch voices for this customer from VAPI
        voices = client.fetch_customer_voices(customer_id)  # Assuming fetch_customer_voices is a method in the SDK
        print(f"Fetched {len(voices)} voices for customer {customer_id}")
        return voices
    except Exception as error:
        print(f"Error fetching voices for customer {customer_id}: {error}")
        raise Exception("Failed to fetch customer voices") from error