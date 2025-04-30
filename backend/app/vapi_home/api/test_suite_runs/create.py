import os
import requests

def create_test_suite_run(test_suite_id):
    api_key = os.getenv('VAPI_PRIVATE_KEY')
    url = f"https://api.vapi.ai/test-suite/{test_suite_id}/run"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, headers=headers, json={})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error creating test suite run: {e}")
        raise

# Example usage
if __name__ == "__main__":
    test_suite_id = "your_test_suite_id"
    try:
        result = create_test_suite_run(test_suite_id)
        print("Created Test Suite Run:", result)
    except Exception as e:
        print(f"Error: {e}")