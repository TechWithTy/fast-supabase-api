import os
import requests

def delete_test_suite_test(test_suite_id: str, test_id: str) -> dict:
    """
    Delete a test from a test suite using the VAPI AI API.

    :param test_suite_id: The ID of the test suite containing the test.
    :param test_id: The ID of the test to delete.
    :return: JSON response data from the API.
    """
    api_key = os.getenv('VAPI_PRIVATE_KEY')
    url = f"https://api.vapi.ai/test-suite/{test_suite_id}/test/{test_id}"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error deleting test suite test: {e}")
        raise