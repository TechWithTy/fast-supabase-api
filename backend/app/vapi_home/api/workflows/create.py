import os
import requests
import json

api_key = os.getenv('VAPI_PRIVATE_KEY')

def create_workflow(name, nodes, edges, model=None):
    url = "https://api.vapi.ai/workflow"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "name": name,
        "nodes": nodes,
        "edges": edges
    }
    
    if model:
        payload["model"] = model
    
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    
    return response.json()

