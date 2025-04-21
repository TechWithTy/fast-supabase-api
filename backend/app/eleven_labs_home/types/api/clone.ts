// import { Readable } from 'stream';

// ElevenLabs Voice Object
export interface ElevenLabsVoice {
  voice_id: string; // The unique identifier of the voice
  name: string; // The name of the voice
  description?: string; // Optional description of the voice
  labels?: Record<string, string>; // Any optional labels for the voice
  // Add other relevant fields here based on the actual API response
}

// ElevenLabs Get Voices Response
export interface GetVoicesResponse {
  voices: ElevenLabsVoice[]; // Array of voices
}

// ElevenLabs Speech Generation Request
export interface GenerateSpeechRequest {
  voice: string; // The ID of the voice to use
  text: string; // The text to generate speech from
  model_id: string; // Model to use (e.g., 'eleven_multilingual_v2')
  // Add more options like language, settings if available
}

// ElevenLabs Client Interface
export interface ElevenLabsClient {
  voices: {
    getAll(): Promise<GetVoicesResponse>; // Method to get all voices
  };
  // generate(request: GenerateSpeechRequest): Promise<Readable>; // Generate speech
}
