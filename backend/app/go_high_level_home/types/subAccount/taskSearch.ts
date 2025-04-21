// Types for Task Search Request
export interface TaskSearchRequest {
  contactId?: string[];
  completed?: boolean;
  assignedTo?: string[];
  query?: string;
  limit?: number;
  skip?: number;
  businessId?: string;
}

// Types for Task Search Response
export interface TaskSearchResponse {
  tasks: any[]; // Adjust this type based on the actual task response structure
}
