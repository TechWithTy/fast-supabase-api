import { GetPhoneNumberResponse } from './get';

// Define the request type for updating a phone number
export interface UpdatePhoneNumberRequest {
  fallbackDestination?: {
    type: 'number';
    numberE164CheckEnabled: boolean;
    number: string;
    extension?: string;
    message?: string;
    description?: string;
  };
  name?: string; // Optional, can be updated
  assistantId?: string;
  squadId?: string;
  serverUrl?: string;
  serverUrlSecret?: string;
}

// Response for updating a phone number is the same as getting one
export type UpdatePhoneNumberResponse = GetPhoneNumberResponse;
