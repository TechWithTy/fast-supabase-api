import os
import requests

api_key = os.getenv('VAPI_PRIVATE_KEY')
url = "https://api.vapi.ai/server"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

payload = {
    "message": {
        "type": "assistant-request"
    }
}

try:
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()
    print("Response:", data)
except requests.exceptions.RequestException as e:
    print("Error:", e)