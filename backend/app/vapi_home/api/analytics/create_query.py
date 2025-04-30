import os
import requests
import json

def create_analytics_query():
    api_key = os.getenv('VAPI_PRIVATE_KEY')
    url = "https://api.vapi.ai/analytics"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "queries": [
            {
                "table": "call",
                "name": "name",
                "operations": [
                    {
                        "operation": "sum",
                        "column": "id"
                    }
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code}, {response.text}"

# Example usage
result = create_analytics_query()
print(json.dumps(result, indent=2))