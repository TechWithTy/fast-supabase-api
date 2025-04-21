// Common Types
export interface CalendarEvent {
  id: string;
  address?: string;
  title: string;
  calendarId: string;
  locationId: string;
  contactId: string;
  groupId: string;
  appointmentStatus: string;
  assignedUserId: string;
  users: string[];
  notes?: string;
  startTime: string; // ISO 8601 date format
  endTime: string; // ISO 8601 date format
  dateAdded: string; // ISO 8601 date format
  dateUpdated: string; // ISO 8601 date format
  assignedResources?: string[];
}

// Request and Response Types
export interface GetCalendarEventsQueryParams {
  calendarId?: string;
  groupId?: string;
  userId?: string;
  endTime: string; // required, ISO 8601 format
  locationId: string; // required
  startTime: string; // required, ISO 8601 format
}

export interface CreateOrUpdateEventRequest {
  calendarId: string;
  locationId: string;
  contactId: string;
  startTime: string;
  endTime: string;
  title: string;
  meetingLocationType?: 'default' | 'custom';
  appointmentStatus?:
    | 'new'
    | 'confirmed'
    | 'cancelled'
    | 'showed'
    | 'noshow'
    | 'invalid';
  assignedUserId?: string;
  address?: string;
  ignoreDateRange?: boolean;
  toNotify?: boolean;
}

export interface BlockSlotRequest {
  calendarId: string;
  locationId: string;
  startTime: string;
  endTime: string;
  title: string;
  assignedUserId: string;
}

export interface GetCalendarEventsResponse {
  events: CalendarEvent[];
}

export interface GetAppointmentResponse {
  event: CalendarEvent;
}

export interface CreateOrUpdateEventResponse {
  calendarId: string;
  locationId: string;
  contactId: string;
  startTime: string;
  endTime: string;
  title: string;
  appointmentStatus: string;
  assignedUserId: string;
  address: string;
  id: string;
}

export interface DeleteEventResponse {
  succeeded: boolean;
}
