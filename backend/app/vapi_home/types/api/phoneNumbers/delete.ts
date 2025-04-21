// Type for DeletePhoneNumberResponse
export interface DeletePhoneNumberResponse {
  fallbackDestination: {
    type: string;
    numberE164CheckEnabled: boolean;
    number: string;
    extension: string;
    message: string;
    description: string;
  };
  provider: 'byo-phone-number';
  numberE164CheckEnabled: boolean;
  id: string;
  orgId: string;
  createdAt: string;
  updatedAt: string;
  name: string;
  assistantId?: string;
  squadId?: string;
  serverUrl?: string;
  serverUrlSecret?: string;
  number: string;
  credentialId: string;
}
