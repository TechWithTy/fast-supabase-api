import { CampaignBase } from '../_dashboard/campaign';

export interface GetEmailByIdResponse {
  id: string; // Required: Email ID
  altId?: string; // Optional: External ID
  threadId: string; // Required: Message or Thread ID
  locationId: string; // Required: Location ID
  contactId: string; // Required: Contact ID
  conversationId: string; // Required: Conversation ID
  dateAdded: string; // Required: Date added (ISO timestamp)
  subject?: string; // Optional: Subject of the email
  body: string; // Required: Body content of the email
  direction: 'inbound' | 'outbound'; // Required: Direction of the email (inbound/outbound)
  status:
    | 'pending'
    | 'scheduled'
    | 'sent'
    | 'delivered'
    | 'read'
    | 'undelivered'
    | 'connected'
    | 'failed'
    | 'opened'; // Allowed status values
  contentType: string; // Required: Content type (e.g., text/plain)
  attachments?: string[]; // Optional: Array of attachment URLs
  provider: 'Leadconnector' | 'Gmail' | 'mailgun' | 'smtp' | 'custom'; // Allowed email providers
  from: string; // Required: Name and email of the sender
  to: string[]; // Required: List of recipient email IDs
  cc?: string[]; // Optional: List of CC email IDs
  bcc?: string[]; // Optional: List of BCC email IDs
  replyToMessageId?: string; // Optional: Reply-to message ID
  source?: 'workflow' | 'bulk_action' | 'campaign' | 'api' | 'app'; // Optional: Source of the email
}

export interface EmailCampaign extends CampaignBase {
  emails: GetEmailByIdResponse[]; // Array of emails associated with the campaign
  senderEmail: string; // The email address that is sending the emails
  recipientCount: number; // Number of recipients
  sentCount: number; // Number of successfully sent emails
  deliveredCount: number; // Number of delivered emails
  openedCount: number; // Number of opened emails
  bouncedCount: number; // Number of bounced emails
  failedCount: number; // Number of failed emails
  workflowID?: string; // ID of the workflow associated with the email campaign (optional)
  funnelID?: string; // ID of the funnel associated with the campaign (optional)
  scriptID?: string; // ID of the script being used (optional)
}

export interface EmailCampaignAnalytics extends CampaignBase {
  emails: GetEmailByIdResponse[]; // Array of emails in the campaign
  senderEmail: string; // Sender email address
  recipientCount: number; // Total number of recipients
  sentCount: number; // Successfully sent emails
  deliveredCount: number; // Successfully delivered emails
  openedCount: number; // Emails opened by recipients
  bouncedCount: number; // Emails that bounced
  failedCount: number; // Emails that failed to send
  workflowID?: string; // Optional workflow associated with the email campaign
  funnelID?: string; // Optional funnel associated with the campaign
  scriptID?: string; // Optional script being used in the campaign
}
