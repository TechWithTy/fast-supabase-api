from typing import List, Union, Optional
from dataclasses import dataclass

@dataclass
class ConversationProviderOutboundMessage:
    """
    Represents an outbound message from a conversation provider.

    Called whenever a user sends a message to a contact and has a custom provider
    as the default channel in the settings.

    Note: This structure differs from other webhooks. Only the fields listed here
    are necessary for successful execution.

    Supported Channels and Modules:
    - SMS: Web App, Mobile App, Workflows, Bulk Actions
    - Email: Web App, Mobile App, Workflows, Bulk Actions
    """

    contact_id: str
    location_id: str
    message_id: str
    type: str
    attachments: List[str]
    user_id: str
    email_message_id: Optional[str] = None
    message: Optional[str] = None
    phone: Optional[str] = None
    email_to: Optional[List[str]] = None
    email_from: Optional[str] = None
    html: Optional[str] = None
    subject: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'ConversationProviderOutboundMessage':
        return cls(
            contact_id=data['contactId'],
            location_id=data['locationId'],
            message_id=data['messageId'],
            type=data['type'],
            attachments=data.get('attachments', []),
            user_id=data['userId'],
            email_message_id=data.get('emailMessageId'),
            message=data.get('message'),
            phone=data.get('phone'),
            email_to=data.get('emailTo'),
            email_from=data.get('emailFrom'),
            html=data.get('html'),
            subject=data.get('subject')
        )

# Example usage:
sms_example = {
    "contactId": "GKBhT6BfwY9mjzXAU3sq",
    "locationId": "GKAWb4yu7A4LSc0skQ6g",
    "messageId": "GKJxs4P5L8dWc5CFUITM",
    "type": "SMS",
    "phone": "+15864603685",
    "message": "The text message to be sent to the contact",
    "attachments": ["https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png"],
    "userId": "GK56r6wdJDrkUPd0xsmx"
}

email_example = {
    "contactId": "GKKFF0QB9gV8fGA6zEbr",
    "locationId": "GKifVDyQeo7nwe27vMP0",
    "messageId": "GK56r6wdJDrkUPd0xsmx",
    "emailMessageId": "GK56r6wdJDrkUPd0xsmx",
    "type": "Email",
    "emailTo": ["abc@gmail.com"],
    "emailFrom": "From Name <email@gmail.com>",
    "attachments": ["https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png"],
    "html": "<div style=\"font-family: verdana, geneva; font-size: 11pt;\"><p>Testing an outbound email from custom provider.</p></div>",
    "subject": "Subject from Conversation Page",
    "userId": "GK56r6wdJDrkUPd0xsmx"
}

sms_message = ConversationProviderOutboundMessage.from_dict(sms_example)
email_message = ConversationProviderOutboundMessage.from_dict(email_example)