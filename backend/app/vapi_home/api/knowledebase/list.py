import os
import requests

def list_knowledge_bases():
    api_key = os.getenv('VAPI_PRIVATE_KEY')
    url = "https://api.vapi.ai/knowledge-base"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response.json()

if __name__ == "__main__":
    try:
        knowledge_bases = list_knowledge_bases()
        print(knowledge_bases)
    except requests.RequestException as e:
        print(f"An error occurred: {e}")