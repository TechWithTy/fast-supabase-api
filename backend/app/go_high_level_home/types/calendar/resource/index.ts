// Common Types
export interface CalendarResource {
  locationId: string;
  name: string;
  resourceType: 'equipments' | 'rooms';
  isActive: boolean;
  description?: string;
  quantity?: number;
  outOfService?: number;
  capacity?: number;
  calendarIds: string[];
}

// Request and Response Types
export interface GetCalendarResourceResponse extends CalendarResource {}

export interface CreateOrUpdateResourceRequest {
  locationId: string;
  name: string;
  description?: string;
  quantity?: number;
  outOfService?: number;
  capacity?: number;
  calendarIds: string[];
  isActive: boolean;
}

export interface ListCalendarResourcesParams {
  limit: number;
  locationId: string;
  skip: number;
}

export interface ListCalendarResourcesResponse {
  resources: CalendarResource[];
}

export interface DeleteCalendarResourceResponse {
  success: boolean;
}
