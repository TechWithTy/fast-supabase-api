import os
import requests

def create_knowledge_base(provider):
    api_key = os.getenv('VAPI_PRIVATE_KEY')
    url = "https://api.vapi.ai/knowledge-base"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "provider": provider
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    return response.json()