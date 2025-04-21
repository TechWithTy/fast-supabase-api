// Assuming AssistantResponse is already declared, we'll reuse it here.

import { AssistantResponse } from './get';

// Type for the response of listing assistants
export interface ListAssistantsResponse {
  assistants: AssistantResponse[]; // Array of assistants
  limit: number; // Maximum number of items returned
  total: number; // Total number of assistants available
}
