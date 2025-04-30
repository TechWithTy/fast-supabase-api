# Example response structure
example_delete_squad_response = {
    "id": "squad-id-123",
    "name": "Example Squad",
    "members": [
        {
            "assistantId": "assistant-id-001",
            "assistant": {
                "transcriber": {
                    "provider": "deepgram",
                    "model": "nova-2",
                    "language": "en"
                },
                "model": {
                    "messages": [
                        {"content": "Hello, how can I help you?", "role": "assistant"}
                    ],
                    "provider": "anyscale",
                    "temperature": 0.7
                }
            }
        }
    ],
    "membersOverrides": {
        "transcriber": {
            "provider": "deepgram",
            "model": "nova-2"
        }
    },
    "orgId": "org-id-001",
    "createdAt": "2023-09-07T12:00:00Z",
    "updatedAt": "2023-09-07T12:30:00Z"
}


# Example response structure
example_get_squad_response = {
    "id": "squad-id-123",
    "name": "Support Team",
    "members": [
        {
            "assistantId": "assistant-id-001",
            "name": "Support Assistant"
        }
    ],
    "createdAt": "2023-09-07T12:00:00Z",
    "updatedAt": "2023-09-07T12:30:00Z"
}

# Example response
example_list_squads_response = {
    "squads": [
        {
            "id": "squad-001",
            "name": "Support Squad",
            "members": [
                {
                    "assistantId": "assistant-001",
                    "assistant": {"transcriber": {"provider": "deepgram", "model": "nova"}}
                }
            ],
            "createdAt": "2023-09-07T12:00:00Z",
            "updatedAt": "2023-09-07T12:10:00Z",
            "membersOverrides": {
                "assistant": {"voice": {"provider": "azure", "voiceId": "andrew"}}
            }
        }
    ]
}
