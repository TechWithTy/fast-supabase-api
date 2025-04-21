import { CustomField, AttributionSource } from './contact';

export type ContactListItem = {
  id: string; // Contact ID
  locationId: string; // Location ID
  email: string; // Contact email
  timezone: string; // Timezone
  country: string; // Country code
  source: string; // Source of the contact (e.g., form submission)
  dateAdded: string; // Date the contact was added (ISO string)
  customFields: CustomField[]; // Array of custom fields
  tags: string[]; // Array of tags associated with the contact
  businessId: string; // Business ID associated with the contact
  attributions?: AttributionSource[]; // Array of attribution sources (optional)
  followers: string[]; // Array of follower IDs
};

export type GetContactsListResponse = {
  contacts: ContactListItem[]; // Array of contacts
  count: number; // Total number of contacts returned
};

export type GetContactsListQueryParams = {
  locationId: string; // Required location ID for querying contacts
  limit?: number; // Limit of records per page (default: 20, max: 100)
  query?: string; // Optional contact search query
  startAfter?: number; // Optional start timestamp
  startAfterId?: string; // Optional start after a specific contact ID
};

export type GetContactsListHeaders = {
  Authorization: string; // Bearer token for authorization
  Version: string; // API version (e.g., '2021-07-28')
};

export const exampleGetContactsListResponse: GetContactsListResponse = {
  contacts: [
    {
      id: 'ocQHyuzHvysMo5N5VsXc',
      locationId: 'C2QujeCh8ZnC7al2InWR',
      email: 'JohnDeo@gmail.com',
      timezone: 'Asia/Calcutta',
      country: 'DE',
      source: 'xyz form',
      dateAdded: '2020-10-29T09:31:30.255Z',
      customFields: [
        {
          id: 'MgobCB14YMVKuE4Ka8p1',
          value: 'name'
        }
      ],
      tags: ['nisi sint commodo amet', 'consequat'],
      businessId: '641c094001436dbc2081e642',
      attributions: [
        {
          url: 'Trigger Link',
          campaign: 'string',
          utmSource: 'string',
          utmMedium: 'string',
          utmContent: 'string',
          referrer: 'https://www.google.com',
          campaignId: 'string',
          fbclid: 'string',
          gclid:
            'CjOKCQjwnNyUBhCZARISAI9AYIFtNnIcWcYGIOQINz_ZoFI5SSLRRugSoPZoiEu27IZBY£1-MAIWmEaAo2VEALW_WCB',
          msclikid: 'string',
          dclid: 'string',
          fbc: 'string',
          fbp: 'fb.1.1674748390986.1171287961',
          fbEventId: 'Mozilla/5.0',
          userAgent: 'Mozilla/5.0',
          ip: '58.111.106.198',
          medium: 'survey',
          mediumId: 'FglfHAn30PRwsZVyQlKp'
        }
      ],
      followers: ['641c094001436dbc2081e642']
    }
  ],
  count: 10
};
