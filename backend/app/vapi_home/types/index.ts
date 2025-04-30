// VAPI Sync Voice Request
export interface VAPISyncVoiceRequest {
  customerId: string; // The ID of the customer
  voiceId: string; // The ID of the voice to sync with VAPI
}

// VAPI Customer Voice Object
export interface VAPICustomerVoice {
  voiceId: string; // The unique identifier of the voice in VAPI
  name: string; // The name of the voice
  description?: string; // Optional description of the voice
  syncedAt: Date; // Date when the voice was synced with VAPI
}

// VAPI Fetch Voices Response
export interface FetchCustomerVoicesResponse {
  voices: VAPICustomerVoice[]; // Array of customer-specific voices
}

// VAPI Client Interface
export interface VAPIClient {
  syncVoice(request: VAPISyncVoiceRequest): Promise<void>; // Sync a voice with VAPI
  fetchCustomerVoices(customerId: string): Promise<FetchCustomerVoicesResponse>; // Fetch voices for a customer
}
