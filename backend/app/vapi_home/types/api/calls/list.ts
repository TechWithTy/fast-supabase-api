// Import existing types
import { GetCallResponse } from '@/types/vapiAi/api/calls/get';

// Query parameters for listing calls
export interface ListCallsQueryParams {
  assistantId?: string; // Filter by assistant ID
  limit?: number; // Maximum number of items to return
  createdAtGt?: string; // Created at greater than
  createdAtLt?: string; // Created at less than
  createdAtGe?: string; // Created at greater than or equal
  createdAtLe?: string; // Created at less than or equal
  updatedAtGt?: string; // Updated at greater than
  updatedAtLt?: string; // Updated at less than
  updatedAtGe?: string; // Updated at greater than or equal
  updatedAtLe?: string; // Updated at less than or equal
}

// Response for list calls (an array of individual call responses)
export interface ListCallsResponse {
  calls: GetCallResponse[]; // Array of individual calls
  totalCount?: number; // Total count of calls, if provided by the API
}
