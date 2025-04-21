// TimeRange used in both the request and response
export interface TimeRange {
  step: 'minute' | 'hour' | 'day' | 'week'; // Time granularity
  start: string; // ISO 8601 start time
  end: string; // ISO 8601 end time
  timezone: string; // Timezone in IANA format (e.g. "UTC", "America/New_York")
}

// Result object for each unique group in the analytics response
export interface AnalyticsResult {
  date: string; // Date in the result (e.g., '2023-01-01')
  assistantId: string; // Assistant ID (if grouped by assistant)
  endedReason?: string; // Reason for call ended (if applicable)
  sumDuration?: number; // Sum of the duration (if 'sum' operation was used)
  avgCost?: number; // Average cost (if 'avg' operation was used)
  [key: string]: any; // For any additional result fields
}

// Response structure for an analytics query
export interface AnalyticsQueryResponse {
  name: string; // Unique key for the query
  timeRange: TimeRange; // Time range used in the query
  result: AnalyticsResult[]; // Result array containing the query's results
}

// Full response type for an analytics query request
export interface AnalyticsResponse {
  data: AnalyticsQueryResponse[]; // Array of query responses
}
