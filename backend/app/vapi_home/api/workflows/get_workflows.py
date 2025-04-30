import os
import requests

api_key = os.getenv('VAPI_PRIVATE_KEY')

def get_workflows():
    url = "https://api.vapi.ai/workflow"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

