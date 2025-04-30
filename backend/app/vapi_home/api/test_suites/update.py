import os
import requests
import json

def update_test_suite(test_suite_id, update_data):
    api_key = os.getenv('VAPI_PRIVATE_KEY')
    url = f"https://api.vapi.ai/test-suite/{test_suite_id}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    response = requests.patch(url, headers=headers, json=update_data)
    response.raise_for_status()
    
    return response.json()

# Example usage
if __name__ == "__main__":
    test_suite_id = "your_test_suite_id"
    update_data = {
        "name": "Updated Test Suite Name",
        # Add other fields you want to update
    }
    
    try:
        updated_test_suite = update_test_suite(test_suite_id, update_data)
        print("Updated Test Suite:", json.dumps(updated_test_suite, indent=2))
    except requests.exceptions.RequestException as e:
        print(f"Error updating test suite: {e}")