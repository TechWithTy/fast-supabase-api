import os
import requests
import json

def update_knowledge_base(knowledge_base_id, provider):
    api_key = os.getenv('VAPI_PRIVATE_KEY')
    url = f"https://api.vapi.ai/knowledge-base/{knowledge_base_id}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "provider": provider
    }

    response = requests.patch(url, headers=headers, json=payload)
    response.raise_for_status()

    return response.json()

# Example usage
# kb_id = "your_knowledge_base_id"
# updated_kb = update_knowledge_base(kb_id, "trieve")
# print(json.dumps(updated_kb, indent=2))