import os
import requests

def create_test_suite(test_suite_data):
    api_key = os.getenv('VAPI_PRIVATE_KEY')
    url = "https://api.vapi.ai/test-suite"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=test_suite_data, headers=headers)
    response.raise_for_status()
    return response.json()

# Example usage
test_suite_data = {
    "name": "Example Test Suite",
    "testerPlan": {
        "assistant": {
            "transcriber": {"provider": "assembly-ai"},
            "model": {"provider": "anyscale", "model": "model"},
            "voice": {"provider": "azure", "voiceId": "andrew"},
            "firstMessage": "Hello! How can I help you today?",
            # Add other necessary fields
        },
        "assistantId": "assistantId",
        # Add other necessary fields
    },
    "targetPlan": {
        "phoneNumberId": "phoneNumberId",
        "phoneNumber": {
            "provider": "test-suite",
            "number": "number"
        }
    },
    "phoneNumberId": "phoneNumberId"
}

try:
    created_test_suite = create_test_suite(test_suite_data)
    print("Created Test Suite:", created_test_suite)
except requests.RequestException as e:
    print(f"Error creating test suite: {e}")