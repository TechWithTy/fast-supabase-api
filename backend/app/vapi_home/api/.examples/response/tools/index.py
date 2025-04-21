example_tool_create_response = {
        "async": False,
        "messages": [
            {
                "type": "tool-message-start",
                "content": "Processing your request, please wait...",
                "role": "assistant"
            }
        ],
        "type": "dtmf",
        "id": "tool-id-123",
        "orgId": "org-id-123",
        "createdAt": "2023-11-07T05:31:56Z",
        "updatedAt": "2023-11-07T05:31:56Z",
        "function": {
            "name": "DTMF Tool",
            "description": "Tool for detecting DTMF tones",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": ["param1"]
            }
        },
        "server": {
            "timeoutSeconds": 20,
            "url": "https://example.com/dtmf-tool",
            "secret": "superSecret"
        }
    }

# Example response format
example_tool_delete_response = {
    "id": "tool-123",
    "status": "deleted",
    "orgId": "org-123",
    "deletedAt": "2023-11-07T05:45:00Z"
}

# Example response format
example_tool_get_response = {
    "id": "23423adasd",
    "async": False,
    "messages": [
        {
            "type": "tool-message-start",
            "content": "Processing your request, please wait...",
            "role": "assistant"
        }
    ],
    "type": "dtmf",
    "orgId": "org-id-123",
    "createdAt": "2023-11-07T05:31:56Z",
    "updatedAt": "2023-11-07T05:31:56Z",
    "function": {
        "name": "DTMF Tool",
        "description": "Tool for detecting DTMF tones",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": ["param1"]
        }
    },
    "server": {
        "timeoutSeconds": 20,
        "url": "https://example.com/dtmf-tool",
        "secret": "superSecret"
    }
}


example_tool_list_response = {
    "tools": [
        {
            "async": False,
            "messages": [
                {
                    "type": "request-start",
                    "content": "Starting the DTMF tool",
                    "conditions": [
                        {
                            "value": "start",
                            "operator": "eq",
                            "param": "trigger"
                        }
                    ]
                }
            ],
            "type": "dtmf",
            "id": "tool-123",
            "orgId": "org-123",
            "createdAt": "2023-11-07T05:31:56Z",
            "updatedAt": "2023-11-07T05:31:56Z",
            "function": {
                "name": "DTMF Function",
                "description": "Detect DTMF tones",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": ["tones"]
                }
            },
            "server": {
                "timeoutSeconds": 20,
                "url": "https://server.url",
                "secret": "superSecretKey"
            }
        }
    ],
    "totalCount": 1
}

example_tool_update_response = {
    "async": False,
    "messages": [
        {
            "type": "request-start",
            "content": "Starting the tool",
            "conditions": [
                {
                    "value": "start",
                    "operator": "eq",
                    "param": "trigger"
                }
            ]
        }
    ],
    "type": "dtmf",
    "id": "tool-123",
    "orgId": "org-123",
    "createdAt": "2023-11-07T05:31:56Z",
    "updatedAt": "2023-11-07T05:32:00Z",
    "function": {
        "name": "Custom Tool Function",
        "description": "This is a custom tool function.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": ["parameter1"]
        }
    },
    "server": {
        "timeoutSeconds": 20,
        "url": "https://custom-server.url",
        "secret": "superSecretKey"
    }
}
