import os
import requests

api_key = os.getenv('VAPI_PRIVATE_KEY')

def delete_workflow(workflow_id):
    url = f"https://api.vapi.ai/workflow/{workflow_id}"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    response = requests.delete(url, headers=headers)
    
    if response.status_code == 200:
        return "Workflow deleted successfully"
    else:
        return f"Error deleting workflow: {response.status_code} - {response.text}"

