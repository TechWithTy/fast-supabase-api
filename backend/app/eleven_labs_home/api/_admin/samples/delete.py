from typing import Dict
from ...client import get_client

def delete_sample(voice_id: str, sample_id: str) -> Dict:
    """
    Deletes a sample for a specific voice.

    Args:
        voice_id (str): The ID of the voice.
        sample_id (str): The ID of the sample to delete.

    Returns:
        Dict: The response from the API.
    """
    client = get_client()
    return client.samples.delete(voice_id=voice_id, sample_id=sample_id)
