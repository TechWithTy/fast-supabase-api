import os
import requests

api_key = os.getenv('VAPI_PRIVATE_KEY')
base_url = 'https://api.vapi.ai'

def get_knowledge_base(knowledge_base_id):
    url = f'{base_url}/knowledge-base/{knowledge_base_id}'
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

# Example usage
# kb_id = 'your_knowledge_base_id'
# result = get_knowledge_base(kb_id)
# print(result)