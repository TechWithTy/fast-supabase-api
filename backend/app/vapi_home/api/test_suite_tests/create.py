import os
import requests

def create_test_suite_test(test_suite_id, test_data):
    api_key = os.getenv('VAPI_PRIVATE_KEY')
    url = f"https://api.vapi.ai/test-suite/{test_suite_id}/test"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=test_data, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error creating test suite test: {e}")
        raise