// Common Types
export interface Template {
  id: string;
  name: string;
  type: 'sms' | 'email' | 'whatsapp';
  template: {
    body: string;
    attachments: string[];
  };
  dateAdded: string;
  locationId: string;
  urlAttachments: string[];
}

export interface GetTemplatesResponse {
  templates: Template[];
  totalCount: number;
}

export interface SubAccount {
  id: string;
  name: string;
  phone: string;
  email: string;
  address: string;
  city: string;
  state: string;
  country: string;
  postalCode: string;
  website: string;
  timezone: string;
  settings?: object;
  social?: object;
}
