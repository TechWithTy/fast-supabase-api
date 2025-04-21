import os
import requests
import json

api_key = os.getenv('VAPI_PRIVATE_KEY')

def get_workflow(workflow_id):
    url = f"https://api.vapi.ai/workflow/{workflow_id}"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    return response.json()

