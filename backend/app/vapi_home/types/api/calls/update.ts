// Import necessary types (assuming they exist in your project)
import { GetCallResponse } from '@/types/vapiAi/api/calls/get'; // Reuse the type from the GET call response

// Type for the request body when updating a call
export interface UpdateCallRequestBody {
  name: string; // This is the name of the call. It is just for your own reference.
}

// Type for the response (can extend the existing GetCallResponse)
export interface UpdateCallResponse extends GetCallResponse {
  // The response will contain similar fields as a GetCallResponse, possibly with updated fields.
}

// Type for the path parameter (call ID)
export interface CallPathParams {
  id: string; // The unique identifier for the call
}
