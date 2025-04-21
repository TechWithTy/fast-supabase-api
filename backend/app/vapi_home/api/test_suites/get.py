import os
import requests

def get_test_suite(test_suite_id):
    api_key = os.getenv('VAPI_PRIVATE_KEY')
    url = f"https://api.vapi.ai/test-suite/{test_suite_id}"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching test suite: {e}")
        return None