import os
import requests

def delete_knowledge_base(knowledge_base_id):
    api_key = os.getenv('VAPI_PRIVATE_KEY')
    url = f"https://api.vapi.ai/knowledge-base/{knowledge_base_id}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    response = requests.delete(url, headers=headers)
    response.raise_for_status()

    return response.json()