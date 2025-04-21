// Enum for Provider Types
export enum PhoneNumberProvider {
  ByoPhoneNumber = 'byo-phone-number',
  TwilioPhoneNumber = 'twilio-phone-number',
  VonagePhoneNumber = 'vonage-phone-number',
  VapiPhoneNumber = 'vapi-phone-number'
}

// Fallback Destination Type
export interface FallbackDestination {
  type: 'number'; // Only 'number' is allowed here
  numberE164CheckEnabled: boolean; // Flag to enable/disable E164 check
  number: string; // The number itself
  extension?: string; // Optional extension
  message?: string; // Message to be used for fallback
  description?: string; // Description of the fallback destination
}

// Request payload for creating a phone number
export interface CreatePhoneNumberRequest {
  fallbackDestination: FallbackDestination; // Fallback configuration
  provider: PhoneNumberProvider; // Use the enum for provider types
  numberE164CheckEnabled: boolean; // E164 check enabled flag
  number: string; // The phone number
  credentialId: string; // SIP trunk/Carrier credential ID
  name: string; // Name for your own reference
  assistantId?: string; // Optional Assistant ID
  squadId?: string; // Optional Squad ID
  serverUrl?: string; // Optional server URL for callbacks
  serverUrlSecret?: string; // Secret sent with every message to the server
}

// Response when a phone number is created
export interface CreatePhoneNumberResponse {
  fallbackDestination: FallbackDestination; // The fallback configuration
  provider: PhoneNumberProvider; // Use the enum for provider types
  numberE164CheckEnabled: boolean; // E164 check enabled flag
  id: string; // Unique identifier for the phone number
  orgId: string; // Unique identifier for the organization
  createdAt: string; // ISO timestamp when the phone number was created
  updatedAt: string; // ISO timestamp when the phone number was last updated
  name: string; // Name for the phone number
  assistantId?: string; // Optional Assistant ID
  squadId?: string; // Optional Squad ID
  serverUrl?: string; // Server URL for callbacks
  serverUrlSecret?: string; // Secret sent with every message to the server
  number: string; // The phone number
  credentialId: string; // SIP trunk/Carrier credential ID
}
