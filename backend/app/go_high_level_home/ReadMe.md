# Go High Level API Integration Template

A comprehensive template for integrating with the Go High Level API, providing pre-implemented functions for all available endpoints. This template simplifies the integration process for developers looking to work with Go High Level's CRM, marketing, and business automation platform.

## Overview

This template provides ready-to-use functions for all Go High Level API endpoints, allowing developers to quickly implement Go High Level integrations in their applications. The template handles authentication, request formatting, and error handling, making it easy to interact with the Go High Level ecosystem.

## Features

- Complete endpoint coverage for Go High Level API
- Authentication handling with API keys and OAuth
- Proper error handling and response parsing
- Pagination support for list endpoints
- Webhook verification and processing

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/go-high-level-template.git
   cd go-high-level-template
   ```

2. Set up your API credentials:
   ```bash
   # Set environment variables
   export GHL_API_KEY="your_api_key"
   export GHL_LOCATION_ID="your_location_id"  # If applicable
   export GHL_COMPANY_ID="your_company_id"    # If applicable
   ```

## Authentication

The template supports both API key authentication and OAuth 2.0:

### API Key Authentication

```python
# Import the GHL client
from ghl_client import GHLClient

# Initialize with API key
client = GHLClient(api_key="your_api_key")

# Or initialize with environment variables
client = GHLClient()
```

### OAuth 2.0 Authentication

```python
# Initialize with OAuth credentials
client = GHLClient(
    client_id="your_client_id",
    client_secret="your_client_secret",
    redirect_uri="your_redirect_uri"
)

# Generate authorization URL
auth_url = client.get_authorization_url()

# Exchange code for tokens
tokens = client.exchange_code_for_tokens("authorization_code")

# Use refresh token to get new access token
new_tokens = client.refresh_access_token("refresh_token")
```

## Available Endpoints

### Contacts

```python
# Create a contact
contact = client.contacts.create({
    "email": "john@example.com",
    "firstName": "John",
    "lastName": "Doe",
    "phone": "+15551234567",
    "customFields": [
        {"id": "custom_field_id", "value": "custom value"}
    ]
})

# Get all contacts
contacts = client.contacts.list(limit=100, page=1)

# Get contact by ID
contact = client.contacts.get("contact_id")

# Update contact
updated_contact = client.contacts.update("contact_id", {
    "firstName": "Johnny"
})

# Delete contact
client.contacts.delete("contact_id")

# Search contacts
search_results = client.contacts.search({
    "query": "john",
    "filters": [
        {"field": "tags", "operator": "contains", "value": "customer"}
    ]
})
```

### Opportunities

```python
# Create an opportunity
opportunity = client.opportunities.create({
    "name": "New Deal",
    "contactId": "contact_id",
    "pipelineId": "pipeline_id",
    "stageId": "stage_id",
    "amount": 5000,
    "status": "open"
})

# Get all opportunities
opportunities = client.opportunities.list(limit=100, page=1)

# Get opportunity by ID
opportunity = client.opportunities.get("opportunity_id")

# Update opportunity
updated_opportunity = client.opportunities.update("opportunity_id", {
    "amount": 7500,
    "status": "won"
})

# Delete opportunity
client.opportunities.delete("opportunity_id")
```

### Pipelines

```python
# Get all pipelines
pipelines = client.pipelines.list()

# Get pipeline by ID
pipeline = client.pipelines.get("pipeline_id")

# Get pipeline stages
stages = client.pipelines.get_stages("pipeline_id")
```

### Appointments

```python
# Create an appointment
appointment = client.appointments.create({
    "title": "Strategy Meeting",
    "description": "Discuss marketing strategy",
    "contactId": "contact_id",
    "startTime": "2023-12-15T10:00:00Z",
    "endTime": "2023-12-15T11:00:00Z",
    "calendarId": "calendar_id"
})

# Get all appointments
appointments = client.appointments.list(
    startDate="2023-12-01",
    endDate="2023-12-31",
    limit=100,
    page=1
)

# Get appointment by ID
appointment = client.appointments.get("appointment_id")

# Update appointment
updated_appointment = client.appointments.update("appointment_id", {
    "title": "Updated Meeting",
    "description": "Updated description"
})

# Cancel appointment
client.appointments.cancel("appointment_id")
```

### Tasks

```python
# Create a task
task = client.tasks.create({
    "title": "Follow up with client",
    "description": "Call to discuss proposal",
    "contactId": "contact_id",
    "dueDate": "2023-12-20",
    "assignedTo": "user_id",
    "status": "not_started"
})

# Get all tasks
tasks = client.tasks.list(limit=100, page=1)

# Get task by ID
task = client.tasks.get("task_id")

# Update task
updated_task = client.tasks.update("task_id", {
    "status": "completed"
})

# Delete task
client.tasks.delete("task_id")
```

### Calendars

```python
# Get all calendars
calendars = client.calendars.list()

# Get calendar by ID
calendar = client.calendars.get("calendar_id")

# Get calendar availability
availability = client.calendars.get_availability("calendar_id", {
    "startDate": "2023-12-01",
    "endDate": "2023-12-31"
})
```

### Forms

```python
# Get all forms
forms = client.forms.list()

# Get form by ID
form = client.forms.get("form_id")

# Get form submissions
submissions = client.forms.get_submissions("form_id", limit=100, page=1)
```

### Campaigns

```python
# Create a campaign
campaign = client.campaigns.create({
    "name": "Holiday Promotion",
    "type": "email",
    "status": "draft"
})

# Get all campaigns
campaigns = client.campaigns.list(limit=100, page=1)

# Get campaign by ID
campaign = client.campaigns.get("campaign_id")

# Update campaign
updated_campaign = client.campaigns.update("campaign_id", {
    "name": "Updated Campaign Name"
})

# Delete campaign
client.campaigns.delete("campaign_id")

# Add contacts to campaign
client.campaigns.add_contacts("campaign_id", ["contact_id1", "contact_id2"])

# Remove contacts from campaign
client.campaigns.remove_contacts("campaign_id", ["contact_id1"])
```

### Workflows

```python
# Get all workflows
workflows = client.workflows.list()

# Get workflow by ID
workflow = client.workflows.get("workflow_id")

# Enroll contacts in workflow
client.workflows.enroll_contacts("workflow_id", ["contact_id1", "contact_id2"])

# Remove contacts from workflow
client.workflows.remove_contacts("workflow_id", ["contact_id1"])
```

### Conversations

```python
# Get all conversations
conversations = client.conversations.list(limit=100, page=1)

# Get conversation by ID
conversation = client.conversations.get("conversation_id")

# Send message
message = client.conversations.send_message({
    "conversationId": "conversation_id",
    "body": "Hello, how can I help you today?",
    "attachments": []
})

# Get conversation messages
messages = client.conversations.get_messages("conversation_id", limit=100, page=1)
```

### Users

```python
# Get all users
users = client.users.list()

# Get user by ID
user = client.users.get("user_id")

# Create a user
new_user = client.users.create({
    "firstName": "Jane",
    "lastName": "Smith",
    "email": "jane@example.com",
    "role": "admin"
})

# Update user
updated_user = client.users.update("user_id", {
    "firstName": "Janet"
})

# Delete user
client.users.delete("user_id")
```

### Locations

```python
# Get all locations
locations = client.locations.list()

# Get location by ID
location = client.locations.get("location_id")
```

### Custom Fields

```python
# Get all custom fields
custom_fields = client.custom_fields.list()

# Get custom field by ID
custom_field = client.custom_fields.get("custom_field_id")

# Create a custom field
new_custom_field = client.custom_fields.create({
    "name": "Preferred Contact Method",
    "type": "dropdown",
    "options": ["Email", "Phone", "Text"],
    "entityType": "contact"
})

# Update custom field
updated_custom_field = client.custom_fields.update("custom_field_id", {
    "name": "Contact Preference"
})

# Delete custom field
client.custom_fields.delete("custom_field_id")
```

### Email Templates

```python
# Get all email templates
templates = client.email_templates.list()

# Get email template by ID
template = client.email_templates.get("template_id")

# Create an email template
new_template = client.email_templates.create({
    "name": "Welcome Email",
    "subject": "Welcome to our company!",
    "body": "<p>Thank you for joining us!</p>"
})

# Update email template
updated_template = client.email_templates.update("template_id", {
    "subject": "Updated Subject"
})

# Delete email template
client.email_templates.delete("template_id")
```

### SMS Templates

```python
# Get all SMS templates
templates = client.sms_templates.list()

# Get SMS template by ID
template = client.sms_templates.get("template_id")

# Create an SMS template
new_template = client.sms_templates.create({
    "name": "Appointment Reminder",
    "body": "Reminder: Your appointment is scheduled for {{appointment_date}}"
})

# Update SMS template
updated_template = client.sms_templates.update("template_id", {
    "body": "Updated message body"
})

# Delete SMS template
client.sms_templates.delete("template_id")
```

### Products

```python
# Get all products
products = client.products.list(limit=100, page=1)

# Get product by ID
product = client.products.get("product_id")

# Create a product
new_product = client.products.create({
    "name": "Premium Service",
    "description": "Our premium service package",
    "price": 299.99,
    "type": "service"
})

# Update product
updated_product = client.products.update("product_id", {
    "price": 249.99
})

# Delete product
client.products.delete("product_id")
```

### Invoices

```python
# Create an invoice
invoice = client.invoices.create({
    "contactId": "contact_id",
    "dueDate": "2023-12-31",
    "items": [
        {"productId": "product_id", "quantity": 1, "price": 299.99}
    ]
})

# Get all invoices
invoices = client.invoices.list(limit=100, page=1)

# Get invoice by ID
invoice = client.invoices.get("invoice_id")

# Update invoice
updated_invoice = client.invoices.update("invoice_id", {
    "status": "sent"
})

# Delete invoice
client.invoices.delete("invoice_id")

# Send invoice
client.invoices.send("invoice_id", {
    "email": "customer@example.com"
})
```

### Payments

```python
# Create a payment
payment = client.payments.create({
    "invoiceId": "invoice_id",
    "amount": 299.99,
    "method": "credit_card",
    "status": "completed"
})

# Get all payments
payments = client.payments.list(limit=100, page=1)

# Get payment by ID
payment = client.payments.get("payment_id")
```

### Membership Sites

```python
# Get all membership sites
sites = client.membership_sites.list()

# Get membership site by ID
site = client.membership_sites.get("site_id")

# Get site members
members = client.membership_sites.get_members("site_id", limit=100, page=1)

# Add members to site
client.membership_sites.add_members("site_id", ["contact_id1", "contact_id2"])

# Remove members from site
client.membership_sites.remove_members("site_id", ["contact_id1"])
```

### Reporting

```python
# Get contact growth report
contact_growth = client.reporting.contact_growth({
    "startDate": "2023-01-01",
    "endDate": "2023-12-31",
    "interval": "month"
})

# Get revenue report
revenue = client.reporting.revenue({
    "startDate": "2023-01-01",
    "endDate": "2023-12-31",
    "interval": "month"
})

# Get campaign performance report
campaign_performance = client.reporting.campaign_performance({
    "campaignId": "campaign_id",
    "startDate": "2023-01-01",
    "endDate": "2023-12-31"
})
```

### Webhooks

```python
# Create a webhook
webhook = client.webhooks.create({
    "url": "https://your-app.com/webhook",
    "events": ["contact.created", "opportunity.updated"]
})

# Get all webhooks
webhooks = client.webhooks.list()

# Get webhook by ID
webhook = client.webhooks.get("webhook_id")

# Update webhook
updated_webhook = client.webhooks.update("webhook_id", {
    "events": ["contact.created", "contact.updated", "opportunity.updated"]
})

# Delete webhook
client.webhooks.delete("webhook_id")
```

## Webhook Processing

Example of processing a Go High Level webhook:

```python
# Flask example
from flask import Flask, request, jsonify
from ghl_client import GHLClient

app = Flask(__name__)
client = GHLClient(api_key="your_api_key")

@app.route('/ghl-webhook', methods=['POST'])
def ghl_webhook():
    # Verify webhook signature
    signature = request.headers.get('X-GHL-Signature')
    is_valid = client.webhooks.verify_signature(
        request.data,
        signature,
        "your_webhook_secret"
    )
    
    if not is_valid:
        return jsonify({"error": "Invalid signature"}), 401
    
    # Process webhook data
    webhook_data = request.json
    event_type = webhook_data.get('event')
    
    if event_type == 'contact.created':
        contact_data = webhook_data.get('data', {})
        # Process new contact
        print(f"New contact created: {contact_data.get('firstName')} {contact_data.get('lastName')}")
    
    return jsonify({"status": "success"}), 200
```

## Pagination

Many list endpoints support pagination:

```python
# Example of handling pagination
all_contacts = []
page = 1
limit = 100

while True:
    contacts_page = client.contacts.list(limit=limit, page=page)
    all_contacts.extend(contacts_page.get('contacts', []))
    
    # Check if we've reached the last page
    total_pages = contacts_page.get('meta', {}).get('totalPages', 0)
    if page >= total_pages:
        break
    
    page += 1

print(f"Total contacts retrieved: {len(all_contacts)}")
```

## Error Handling

The template includes comprehensive error handling:

```python
try:
    contact = client.contacts.get("non_existent_id")
except GHLApiError as e:
    print(f"API Error: {e.status_code} - {e.message}")
    # Handle specific error codes
    if e.status_code == 404:
        print("Contact not found")
except GHLConnectionError as e:
    print(f"Connection Error: {str(e)}")
```

## Multi-Location Support

For agencies or businesses with multiple locations:

```python
# Initialize with specific location
client = GHLClient(api_key="your_api_key", location_id="location_id")

# Or switch location during execution
client.set_location("new_location_id")

# Use company-wide API (agency level)
client.set_company_mode(True)
```

## API Rate Limiting

The template includes rate limit handling:

```python
# Configure rate limit behavior
client.configure_rate_limiting(
    max_retries=3,
    retry_delay=2,  # seconds
    backoff_factor=1.5
)
```

## Resources

- [Go High Level API Documentation](https://highlevel.stoplight.io/docs)
- [Go High Level Developer Center](https://developers.gohighlevel.com/)
- [Go High Level Help Center](https://help.gohighlevel.com/)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

Created and maintained by [Your Name/Organization]