import requests
import json
import os
from datetime import datetime
# https://docs.vapi.ai/server-url/setting-server-urls
# Retrieve API token from environment variables

API_TOKEN = os.getenv("VAPI_PRIVATE_TOKEN")
API_URL = os.getenv("VAPI_API_URL")

HEADERS = {"Authorization": f"Bearer {API_TOKEN}", "Content-Type": "application/json"}


def send_assistant_message(payload: dict):
    """
    Send an assistant request message to the server.

    :param payload: A dictionary containing the message request payload.
    :return: JSON response data or None if an error occurs.
    """
    if not API_TOKEN:
        print(
            "Error: Missing API token. Set VAPI_PRIVATE_TOKEN in your environment variables."
        )
        return None

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        data = response.json()

        print("Server response:", json.dumps(data, indent=4))
        return data

    except requests.exceptions.RequestException as err:
        print("Error:", err)
        return None


example_assistant_message_payload = {
        "message": {
            "type": "assistant-request",
            "assistant": {"id": "assistant-123", "name": "Assistant Name"},
            "phoneNumber": {"id": "phone-123", "number": "+14155551234"},
            "customer": {"id": "customer-123", "name": "John Doe"},
            "call": {"id": "call-123", "status": "in-progress"},
            "artifact": {
                "recording": "https://example.com/recording.mp3",
                "transcription": "Hello, how can I help you?",
            },
            "timestamp": datetime.utcnow().isoformat(),  # Current UTC timestamp
        }
    }
