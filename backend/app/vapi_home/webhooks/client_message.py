import os
import requests

def send_client_message():
    api_key = os.getenv('VAPI_PRIVATE_KEY')
    url = "https://api.vapi.ai/client"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "message": {
            "type": "workflow.node.started",
            "node": {
                "key": "value"
            }
        }
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")