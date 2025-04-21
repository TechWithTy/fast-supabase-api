import { CampaignBase } from '../_dashboard/campaign';

// Restrict the messageType to be either 'SMS' or 'EMAIL'
export type MessageType = 'TYPE_SMS' | 'TYPE_EMAIL';

export interface GetMessagesByConversationIdRequest {
  conversationId: string; // Conversation ID as string
  lastMessageId?: string; // Optional: Last message ID for pagination
  limit?: number; // Optional: Number of messages to fetch (default 20)
  type?: MessageType; // The type of messages to fetch, either 'SMS' or 'EMAIL'
}

// Types for the response of the message API
export interface GetMessagesByConversationIdResponse {
  lastMessageId: string; // Id of the last message in the array
  nextPage: boolean; // Boolean indicating if there are more pages of messages
  messages: Message[]; // Array of message objects
}

// Message type structure, limited to SMS or EMAIL
export interface TextMessage {
  id: string; // Message ID
  type: number; // Type as a number (e.g., 1 for SMS, 3 for EMAIL)
  messageType: MessageType; // Type of message (either 'SMS' or 'EMAIL')
  locationId: string; // Location ID
  contactId: string; // Contact ID
  conversationId: string; // Conversation ID
  dateAdded: string; // ISO timestamp of when the message was added
  body?: string; // Message body (e.g., the SMS text or email content)
  direction: 'inbound' | 'outbound'; // Direction of the message (inbound or outbound)
  status:
    | 'pending'
    | 'scheduled'
    | 'sent'
    | 'delivered'
    | 'read'
    | 'undelivered'
    | 'connected'
    | 'failed'
    | 'opened'; // Status of the message
  contentType: string; // Content type (e.g., "text/plain")
  attachments?: string[]; // Optional array of attachment URLs
  meta?: Meta; // Optional meta object for additional data (e.g., emails)
  source?: 'workflow' | 'bulk_actions' | 'campaign' | 'api' | 'app'; // Optional: source of the message
  userId?: string; // Optional: User ID
}

// Meta data for the message (used for email-type messages)
export interface Meta {
  email?: {
    messageIds: string[]; // List of all email message IDs in the thread
  };
}

export interface GHLTextMessageCampaign extends CampaignBase {
  id: string; // Campaign ID
  name: string; // Campaign name
  createdAt: string; // Date when the campaign was created (ISO string)
  sentCount: number; // Number of messages sent
  deliveredCount: number; // Number of messages delivered
  failedCount: number; // Number of messages failed
  totalMessages: number; // Total messages in the campaign
  lastMessageSentAt: string; // Date when the last message was sent
  conversationId: string;
  messages: TextMessage[]; // ID of the conversation associated with the campaign
}

export interface TextMessageCampaignAnalytics extends CampaignBase {
  id: string; // Campaign ID
  name: string; // Campaign name
  createdAt: string; // Date when the campaign was created
  sentCount: number; // Number of SMS sent
  deliveredCount: number; // Number of SMS delivered
  failedCount: number; // Number of SMS that failed to send
  totalMessages: number; // Total SMS messages in the campaign
  lastMessageSentAt: string; // Timestamp of the last message sent
  conversationId: string; // Associated conversation ID
  messages: TextMessage[]; // Array of messages in the campaign
}

export interface SendMessageRequest {
  type:
    | 'SMS'
    | 'Email'
    | 'WhatsApp'
    | 'GMB'
    | 'IG'
    | 'FB'
    | 'Custom'
    | 'Live_Chat';
  contactId: string;
  appointmentId?: string;
  attachments?: string[];
  emailFrom?: string;
  emailCc?: string[];
  emailBcc?: string[];
  html?: string;
  message?: string;
  subject?: string;
  replyMessageId?: string;
  templateId?: string;
  scheduledTimestamp?: number;
  conversationProviderId?: string;
  emailTo?: string;
  emailReplyMode?: 'reply' | 'reply_all';
}

export interface SendMessageResponse {
  conversationId: string;
  emailMessageId?: string;
  messageId: string;
  messageIds?: string[];
  msg?: string;
}

export interface AddInboundMessageRequest {
  type:
    | 'SMS'
    | 'Email'
    | 'WhatsApp'
    | 'GMB'
    | 'IG'
    | 'FB'
    | 'Custom'
    | 'WebChat'
    | 'Live_Chat'
    | 'Call';
  attachments?: string[];
  message?: string;
  conversationId: string;
  conversationProviderId: string;
  html?: string;
  subject?: string;
  emailFrom?: string;
  emailTo?: string;
  emailCc?: string[];
  emailBcc?: string[];
  emailMessageId?: string;
  altId?: string;
  direction?: 'outbound' | 'inbound';
  date?: string;
  call?: {
    to: string;
    from: string;
    status:
      | 'pending'
      | 'completed'
      | 'answered'
      | 'busy'
      | 'no-answer'
      | 'failed'
      | 'canceled'
      | 'voicemail';
  };
}

export interface CancelScheduledMessageResponse {
  status: number;
  message: string;
}
export interface AddInboundMessageResponse {
  success: boolean;
  conversationId: string;
  messageId: string;
  message: string;
  contactId: string;
  dateAdded: string;
  emailMessageId?: string;
}

export interface AddOutboundCallRequest {
  type: 'Call';
  attachments?: string[];
  conversationId: string;
  conversationProviderId: string;
  altId?: string;
  date?: string;
  call?: {
    to: string;
    from: string;
    status:
      | 'pending'
      | 'completed'
      | 'answered'
      | 'busy'
      | 'no-answer'
      | 'failed'
      | 'canceled'
      | 'voicemail';
  };
}

export interface AddOutboundCallResponse {
  success: boolean;
  conversationId: string;
  messageId: string;
  message: string;
  contactId: string;
  dateAdded: string;
  emailMessageId?: string;
}

export interface UpdateMessageStatusResponse {
  conversationId: string;
  emailMessageId?: string;
  messageId: string;
  messageIds?: string[];
  msg?: string;
}

export interface UpdateMessageStatusRequest {
  status: 'read' | 'pending' | 'delivered' | 'failed';
  error?: {
    code: string;
    type: string;
    message: string;
  };
  emailMessageId?: string;
  recipients?: string[];
}
