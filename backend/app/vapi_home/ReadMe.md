# VAPI API Integration Template

This template provides pre-implemented functions for all VAPI endpoints, making it suitable for creating an SDK or streamlining API integration with Python applications. Each endpoint function is already implemented with proper request formatting and error handling.

## Overview

[VAPI](https://vapi.ai/) is a platform for building AI voice applications that can handle phone calls, voice messaging, and other voice-based interactions. This template simplifies the integration process with pre-built functions for all available endpoints.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/vapi-python-template.git
   cd vapi-python-template
   ```

2. Install required dependencies:
   ```bash
   pip install requests  # Or other HTTP client library used in the template
   ```

3. Set your VAPI API key:
   ```python
   # In your code
   VAPI_API_KEY = "your_api_key_here"
   
   # Or as an environment variable
   # export VAPI_API_KEY="your_api_key_here"
   ```

## Authentication

All functions in the template handle authentication automatically by including your API key in the headers:

```python
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}
```

## Available Endpoints

### Phone Calls

#### Create a Call

```python
def create_call(recipient_number, assistant_id, caller_id=None, webhook_url=None, webhook_events=None):
    """
    Start a new phone call.
    
    Args:
        recipient_number (str): Phone number to call (E.164 format)
        assistant_id (str): ID of the assistant to use for the call
        caller_id (str, optional): Phone number to show as caller ID
        webhook_url (str, optional): URL to receive webhook events
        webhook_events (list, optional): List of webhook events to subscribe to
        
    Returns:
        dict: Call details including call_id
    """
    # Implementation already available in template
```

#### List Calls

```python
def list_calls(limit=10, offset=0, status=None):
    """
    List phone calls with pagination and optional filtering.
    
    Args:
        limit (int, optional): Maximum number of calls to return
        offset (int, optional): Pagination offset
        status (str, optional): Filter by call status
        
    Returns:
        dict: List of calls and pagination metadata
    """
    # Implementation already available in template
```

#### Get Call Details

```python
def get_call(call_id):
    """
    Get details about a specific call.
    
    Args:
        call_id (str): ID of the call to retrieve
        
    Returns:
        dict: Call details
    """
    # Implementation already available in template
```

#### End Call

```python
def end_call(call_id):
    """
    End an active call.
    
    Args:
        call_id (str): ID of the call to end
        
    Returns:
        dict: Updated call details
    """
    # Implementation already available in template
```

### Assistants

#### Create Assistant

```python
def create_assistant(name, voice, first_message, model="gpt-4", instructions=None, metadata=None):
    """
    Create a new voice assistant.
    
    Args:
        name (str): Name of the assistant
        voice (str): Voice ID to use (e.g., "shimmer", "echo", "nova")
        first_message (str): First message the assistant will say
        model (str, optional): Language model to use
        instructions (str, optional): Custom instructions for the assistant
        metadata (dict, optional): Custom metadata
        
    Returns:
        dict: Created assistant details
    """
    # Implementation already available in template
```

#### List Assistants

```python
def list_assistants(limit=10, offset=0):
    """
    List voice assistants with pagination.
    
    Args:
        limit (int, optional): Maximum number of assistants to return
        offset (int, optional): Pagination offset
        
    Returns:
        dict: List of assistants and pagination metadata
    """
    # Implementation already available in template
```

#### Get Assistant

```python
def get_assistant(assistant_id):
    """
    Get details about a specific assistant.
    
    Args:
        assistant_id (str): ID of the assistant to retrieve
        
    Returns:
        dict: Assistant details
    """
    # Implementation already available in template
```

#### Update Assistant

```python
def update_assistant(assistant_id, updates):
    """
    Update an existing assistant.
    
    Args:
        assistant_id (str): ID of the assistant to update
        updates (dict): Fields to update
        
    Returns:
        dict: Updated assistant details
    """
    # Implementation already available in template
```

#### Delete Assistant

```python
def delete_assistant(assistant_id):
    """
    Delete an assistant.
    
    Args:
        assistant_id (str): ID of the assistant to delete
        
    Returns:
        dict: Deletion confirmation
    """
    # Implementation already available in template
```

### Phone Numbers

#### List Phone Numbers

```python
def list_phone_numbers(limit=10, offset=0):
    """
    List phone numbers associated with your account.
    
    Args:
        limit (int, optional): Maximum number of phone numbers to return
        offset (int, optional): Pagination offset
        
    Returns:
        dict: List of phone numbers and pagination metadata
    """
    # Implementation already available in template
```

#### Get Phone Number

```python
def get_phone_number(phone_number_id):
    """
    Get details about a specific phone number.
    
    Args:
        phone_number_id (str): ID of the phone number to retrieve
        
    Returns:
        dict: Phone number details
    """
    # Implementation already available in template
```

#### Update Phone Number

```python
def update_phone_number(phone_number_id, assistant_id=None, webhook_url=None, webhook_events=None):
    """
    Update configuration for a phone number.
    
    Args:
        phone_number_id (str): ID of the phone number to update
        assistant_id (str, optional): ID of the assistant to use for inbound calls
        webhook_url (str, optional): URL to receive webhook events
        webhook_events (list, optional): List of webhook events to subscribe to
        
    Returns:
        dict: Updated phone number details
    """
    # Implementation already available in template
```

### Messages

#### Send Message

```python
def send_message(to_number, assistant_id, content, from_number=None, webhook_url=None):
    """
    Send a voice message to a phone number.
    
    Args:
        to_number (str): Phone number to send the message to (E.164 format)
        assistant_id (str): ID of the assistant to use for the message
        content (str): Text content of the message
        from_number (str, optional): Phone number to send from
        webhook_url (str, optional): URL to receive webhook events
        
    Returns:
        dict: Message details including message_id
    """
    # Implementation already available in template
```

#### List Messages

```python
def list_messages(limit=10, offset=0, status=None):
    """
    List messages with pagination and optional filtering.
    
    Args:
        limit (int, optional): Maximum number of messages to return
        offset (int, optional): Pagination offset
        status (str, optional): Filter by message status
        
    Returns:
        dict: List of messages and pagination metadata
    """
    # Implementation already available in template
```

#### Get Message

```python
def get_message(message_id):
    """
    Get details about a specific message.
    
    Args:
        message_id (str): ID of the message to retrieve
        
    Returns:
        dict: Message details
    """
    # Implementation already available in template
```

### Test Suites

#### Create Test Suite

```python
def create_test_suite(name, assistant_id, description=None):
    """
    Create a new test suite for an assistant.
    
    Args:
        name (str): Name of the test suite
        assistant_id (str): ID of the assistant to test
        description (str, optional): Description of the test suite
        
    Returns:
        dict: Created test suite details
    """
    # Implementation already available in template
```

#### List Test Suites

```python
def list_test_suites(limit=10, offset=0):
    """
    List test suites with pagination.
    
    Args:
        limit (int, optional): Maximum number of test suites to return
        offset (int, optional): Pagination offset
        
    Returns:
        dict: List of test suites and pagination metadata
    """
    # Implementation already available in template
```

#### Get Test Suite

```python
def get_test_suite(test_suite_id):
    """
    Get details about a specific test suite.
    
    Args:
        test_suite_id (str): ID of the test suite to retrieve
        
    Returns:
        dict: Test suite details
    """
    # Implementation already available in template
```

#### Update Test Suite

```python
def update_test_suite(test_suite_id, updates):
    """
    Update an existing test suite.
    
    Args:
        test_suite_id (str): ID of the test suite to update
        updates (dict): Fields to update
        
    Returns:
        dict: Updated test suite details
    """
    # Implementation already available in template
```

#### Delete Test Suite

```python
def delete_test_suite(test_suite_id):
    """
    Delete a test suite.
    
    Args:
        test_suite_id (str): ID of the test suite to delete
        
    Returns:
        dict: Deletion confirmation
    """
    # Implementation already available in template
```

#### Run Test Suite

```python
def run_test_suite(test_suite_id):
    """
    Run a test suite.
    
    Args:
        test_suite_id (str): ID of the test suite to run
        
    Returns:
        dict: Test run details including run_id
    """
    # Implementation already available in template
```

### Test Cases

#### Create Test Case

```python
def create_test_case(test_suite_id, name, conversation_turns, description=None):
    """
    Create a new test case within a test suite.
    
    Args:
        test_suite_id (str): ID of the test suite
        name (str): Name of the test case
        conversation_turns (list): List of conversation turn objects
        description (str, optional): Description of the test case
        
    Returns:
        dict: Created test case details
    """
    # Implementation already available in template
```

#### List Test Cases

```python
def list_test_cases(test_suite_id, limit=10, offset=0):
    """
    List test cases for a test suite with pagination.
    
    Args:
        test_suite_id (str): ID of the test suite
        limit (int, optional): Maximum number of test cases to return
        offset (int, optional): Pagination offset
        
    Returns:
        dict: List of test cases and pagination metadata
    """
    # Implementation already available in template
```

#### Get Test Case

```python
def get_test_case(test_case_id):
    """
    Get details about a specific test case.
    
    Args:
        test_case_id (str): ID of the test case to retrieve
        
    Returns:
        dict: Test case details
    """
    # Implementation already available in template
```

#### Update Test Case

```python
def update_test_case(test_case_id, updates):
    """
    Update an existing test case.
    
    Args:
        test_case_id (str): ID of the test case to update
        updates (dict): Fields to update
        
    Returns:
        dict: Updated test case details
    """
    # Implementation already available in template
```

#### Delete Test Case

```python
def delete_test_case(test_case_id):
    """
    Delete a test case.
    
    Args:
        test_case_id (str): ID of the test case to delete
        
    Returns:
        dict: Deletion confirmation
    """
    # Implementation already available in template
```

### Custom Voices

#### Create Custom Voice

```python
def create_custom_voice(name, samples, description=None):
    """
    Create a new custom voice.
    
    Args:
        name (str): Name of the custom voice
        samples (list): List of audio samples (base64 encoded)
        description (str, optional): Description of the custom voice
        
    Returns:
        dict: Created custom voice details
    """
    # Implementation already available in template
```

#### List Custom Voices

```python
def list_custom_voices(limit=10, offset=0):
    """
    List custom voices with pagination.
    
    Args:
        limit (int, optional): Maximum number of custom voices to return
        offset (int, optional): Pagination offset
        
    Returns:
        dict: List of custom voices and pagination metadata
    """
    # Implementation already available in template
```

#### Get Custom Voice

```python
def get_custom_voice(custom_voice_id):
    """
    Get details about a specific custom voice.
    
    Args:
        custom_voice_id (str): ID of the custom voice to retrieve
        
    Returns:
        dict: Custom voice details
    """
    # Implementation already available in template
```

#### Delete Custom Voice

```python
def delete_custom_voice(custom_voice_id):
    """
    Delete a custom voice.
    
    Args:
        custom_voice_id (str): ID of the custom voice to delete
        
    Returns:
        dict: Deletion confirmation
    """
    # Implementation already available in template
```

### Webhooks

```python
def verify_webhook_signature(payload, signature, secret):
    """
    Verify the signature of a webhook event.
    
    Args:
        payload (str): Raw webhook payload
        signature (str): Signature from the X-VAPI-Signature header
        secret (str): Your webhook secret
        
    Returns:
        bool: Whether the signature is valid
    """
    # Implementation already available in template
```

## Data Types

### Call Object

```python
{
    "id": "call_abc123",
    "object": "call",
    "created_at": "2023-01-01T12:00:00.000Z",
    "updated_at": "2023-01-01T12:05:00.000Z",
    "status": "completed",  # queued, ringing, in-progress, completed, failed
    "duration": 300,  # seconds
    "recipient": {
        "phone_number": "+15551234567"
    },
    "caller": {
        "phone_number": "+15559876543"
    },
    "assistant_id": "asst_abc123",
    "metadata": { }
}
```

### Assistant Object

```python
{
    "id": "asst_abc123",
    "object": "assistant",
    "created_at": "2023-01-01T12:00:00.000Z",
    "updated_at": "2023-01-01T12:05:00.000Z",
    "name": "Customer Support",
    "model": "gpt-4",
    "voice": "shimmer",
    "first_message": "Hello, how can I help you today?",
    "instructions": "You are a helpful customer support agent.",
    "metadata": { }
}
```

### Phone Number Object

```python
{
    "id": "pn_abc123",
    "object": "phone_number",
    "created_at": "2023-01-01T12:00:00.000Z",
    "updated_at": "2023-01-01T12:05:00.000Z",
    "phone_number": "+15551234567",
    "country": "US",
    "active": true,
    "configuration": {
        "assistant_id": "asst_abc123",
        "webhook_url": "https://example.com/webhook",
        "webhook_events": ["call.completed", "call.failed"]
    }
}
```

### Message Object

```python
{
    "id": "msg_abc123",
    "object": "message",
    "created_at": "2023-01-01T12:00:00.000Z",
    "updated_at": "2023-01-01T12:05:00.000Z",
    "status": "delivered",  # queued, sending, delivered, failed
    "to": "+15551234567",
    "from": "+15559876543",
    "assistant_id": "asst_abc123",
    "content": "Hello, this is your reminder about tomorrow's appointment.",
    "duration": 15,  # seconds
    "metadata": { }
}
```

### Test Suite Object

```python
{
    "id": "ts_abc123",
    "object": "test_suite",
    "created_at": "2023-01-01T12:00:00.000Z",
    "updated_at": "2023-01-01T12:05:00.000Z",
    "name": "Customer Support Tests",
    "description": "Tests for the customer support assistant",
    "assistant_id": "asst_abc123",
    "test_cases_count": 5
}
```

### Test Case Object

```python
{
    "id": "tc_abc123",
    "object": "test_case",
    "created_at": "2023-01-01T12:00:00.000Z",
    "updated_at": "2023-01-01T12:05:00.000Z",
    "name": "Order Status Inquiry",
    "description": "Customer asking about order status",
    "test_suite_id": "ts_abc123",
    "conversation_turns": [
        {
            "role": "user",
            "content": "Can you tell me the status of my order?"
        },
        {
            "role": "assistant",
            "expected_response_contains": ["order", "status", "check"]
        }
    ]
}
```

### Custom Voice Object

```python
{
    "id": "cv_abc123",
    "object": "custom_voice",
    "created_at": "2023-01-01T12:00:00.000Z",
    "updated_at": "2023-01-01T12:05:00.000Z",
    "name": "Company Voice",
    "description": "Custom voice for company branding",
    "status": "ready",  # processing, ready, failed
    "samples_count": 3
}
```

## Error Handling

All functions include proper error handling with descriptive error messages:

```python
def example_function():
    try:
        # API request
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # Raise exception for 4XX/5XX responses
        return response.json()
    except requests.exceptions.RequestException as e:
        if hasattr(e, 'response') and e.response is not None:
            error_message = e.response.json().get('message', str(e))
            status_code = e.response.status_code
            raise Exception(f"VAPI API Error ({status_code}): {error_message}")
        else:
            raise Exception(f"VAPI API Connection Error: {str(e)}")
```

## Pagination

Functions that return lists support pagination:

```python
# Example use of pagination
page1 = list_calls(limit=10, offset=0)
page2 = list_calls(limit=10, offset=10)
```

## Webhook Handling

Example of processing a VAPI webhook:

```python
# Flask example
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/vapi-webhook', methods=['POST'])
def vapi_webhook():
    event = request.json
    
    # Verify webhook signature
    signature = request.headers.get('X-VAPI-Signature')
    is_valid = verify_webhook_signature(
        request.data.decode('utf-8'),
        signature,
        "your_webhook_secret"
    )
    
    if not is_valid:
        return jsonify({"error": "Invalid signature"}), 401
    
    # Handle different event types
    event_type = event.get('type')
    
    if event_type == 'call.completed':
        # Handle completed call
        call_id = event.get('data', {}).get('id')
        # Process call data
        
    elif event_type == 'message.delivered':
        # Handle delivered message
        message_id = event.get('data', {}).get('id')
        # Process message data
    
    return jsonify({"status": "success"}), 200
```

## Resources

- [VAPI Documentation](https://docs.vapi.ai/)
- [API Reference](https://docs.vapi.ai/api-reference)