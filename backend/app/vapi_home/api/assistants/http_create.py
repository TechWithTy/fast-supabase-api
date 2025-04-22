"""
HTTP utility for creating a Vapi assistant via the official API.
Follows Vapi API docs: https://docs.vapi.ai/api-reference/assistants/create

Usage:
    from .http_create import create_vapi_assistant
    response = create_vapi_assistant(api_key, assistant_payload)
"""

import requests
from typing import Any, Dict, Optional

def create_vapi_assistant(api_key: str, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Create a Vapi assistant using the HTTP API.

    Args:
        api_key (str): Your Vapi secret (bearer) token.
        payload (dict): The assistant configuration as per Vapi docs.

    Returns:
        dict or None: The created assistant response or None if error.
    """
    url = "https://api.vapi.ai/v1/assistants"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error creating Vapi assistant: {e}\n{getattr(e, 'response', None)}")
        return None
