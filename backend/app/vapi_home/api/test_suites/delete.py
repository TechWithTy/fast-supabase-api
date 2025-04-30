import os
import requests

def delete_test_suite(test_suite_id: str) -> dict:
    """
    Delete a test suite using the VAPI AI API.

    :param test_suite_id: The ID of the test suite to delete.
    :return: JSON response data from the API.
    """
    api_key = os.getenv('VAPI_PRIVATE_KEY')
    url = f"https://api.vapi.ai/test-suite/{test_suite_id}"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.delete(url, headers=headers)
        
        if not response.ok:
            error_text = response.text
            raise Exception(f"Error deleting test suite: {error_text}")
            
        return response.json()
        
    except Exception as err:
        print("Error:", err)
        raise err