import os
import requests

def update_test_suite_run(test_suite_id: str, run_id: str, update_data: dict) -> dict:
    """
    Update a test suite run using the VAPI AI API.

    :param test_suite_id: The ID of the test suite.
    :param run_id: The ID of the run to update.
    :param update_data: A dictionary containing the data to update.
    :return: JSON response data from the API.
    """
    api_key = os.getenv('VAPI_PRIVATE_KEY')
    url = f"https://api.vapi.ai/test-suite/{test_suite_id}/run/{run_id}"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.patch(url, headers=headers, json=update_data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error updating test suite run: {e}")
        raise

# Example usage
if __name__ == "__main__":
    test_suite_id = "testSuiteId"
    run_id = "id"
    update_data = {}  # Add fields to update if needed
    
    try:
        updated_run = update_test_suite_run(test_suite_id, run_id, update_data)
        print("Updated Test Suite Run:", updated_run)
    except Exception as e:
        print(f"Error: {e}")