import os
import requests

def delete_test_suite_run(test_suite_id: str, run_id: str) -> dict:
    """
    Delete a test suite run using the VAPI AI API.

    :param test_suite_id: The ID of the test suite.
    :param run_id: The ID of the run to delete.
    :return: JSON response data from the API.
    """
    api_key = os.getenv('VAPI_PRIVATE_KEY')
    url = f"https://api.vapi.ai/test-suite/{test_suite_id}/run/{run_id}"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error deleting test suite run: {e}")
        raise
