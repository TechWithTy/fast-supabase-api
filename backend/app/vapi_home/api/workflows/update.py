import os
import requests
import json

api_key = os.getenv('VAPI_PRIVATE_KEY')

def update_workflow(workflow_id, data):
    url = f"https://api.vapi.ai/workflow/{workflow_id}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    response = requests.patch(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

# Example usage
workflow_data = {
    "nodes": [
        {
            "type": "say",
            "name": "name",
            "exact": "exact",
            "metadata": {
                "key": "value"
            },
            "prompt": "prompt"
        }
    ],
    "name": "name",
    "edges": [
        {
            "from": "from",
            "to": "to",
            "condition": {
                "type": "ai",
                "matches": [
                    "matches"
                ]
            },
            "metadata": {
                "key": "value"
            }
        }
    ],
    "model": {
        "provider": "anthropic",
        "model": "claude-3-opus-20240229",
        "emotionRecognitionEnabled": True,
        "knowledgeBase": {
            "server": {
                "url": "url",
                "timeoutSeconds": 20,
                "backoffPlan": {
                    "maxRetries": 0,
                    "type": {
                        "key": "value"
                    },
                    "baseDelaySeconds": 1
                }
            }
        },
        "knowledgeBaseId": "knowledgeBaseId",
        "maxTokens": 1.1,
        "messages": [
            {
                "role": "assistant"
            }
        ],
        "numFastTurns": 1.1,
        "temperature": 1.1,
        "thinking": {
            "type": "enabled",
            "budgetTokens": 1.1
        },
        "toolIds": [
            "toolIds"
        ],
        "tools": [
            {
                "type": "dtmf",
                "async": False
            }
        ]
    }
}

try:
    updated_workflow = update_workflow("workflow_id", workflow_data)
    print(json.dumps(updated_workflow, indent=2))
except requests.exceptions.RequestException as e:
    print(f"Error updating workflow: {e}")