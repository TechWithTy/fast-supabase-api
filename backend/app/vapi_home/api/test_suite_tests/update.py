import os
import requests

def update_test_suite_test(test_suite_id: str, test_id: str, update_data: dict) -> dict:
    api_key = os.getenv('VAPI_PRIVATE_KEY')
    url = f"https://api.vapi.ai/test-suite/{test_suite_id}/test/{test_id}"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.patch(url, headers=headers, json=update_data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error updating test suite test: {e}")
        raise

# Example usage
if __name__ == "__main__":
    test_suite_id = "testSuiteId"
    test_id = "id"
    update_data = {
        "type": "voice"
    }
    
    try:
        updated_test = update_test_suite_test(test_suite_id, test_id, update_data)
        print("Updated Test:", updated_test)
    except Exception as e:
        print(f"Error: {e}")