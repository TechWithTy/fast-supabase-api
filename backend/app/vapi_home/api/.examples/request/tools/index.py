example_create_tool_data = {
        "async": False,
        "messages": [
            {
                "type": "tool-message-start",
                "content": "Processing your request, please wait...",
                "role": "assistant"
            }
        ],
        "type": "dtmf",
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