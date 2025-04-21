from typing import Optional
from ..client import get_client
from vapi import CreateByoPhoneNumberDto


def create_phone_number(payload: dict) -> Optional[dict]:
    """
    Create a phone number using the Vapi SDK.

    Args:
        payload (dict): The phone number configuration.

    Returns:
        Optional[dict]: The response from the API if successful, None otherwise.
    """
    try:
        client = get_client()
        return client.phone_numbers.create(request=CreateByoPhoneNumberDto(**payload))
    except Exception as e:
        print(f"Error creating phone number: {e}")
        return None

# Example usage:
create_phone_number(payload={"credential_id": "credentialId"})
