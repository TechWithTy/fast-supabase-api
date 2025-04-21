// Common Types
export interface CalendarNotification {
  type: 'email';
  shouldSendToContact: boolean;
  shouldSendToGuest: boolean;
  shouldSendToUser: boolean;
  shouldSendToSelectedUsers: boolean;
  selectedUsers: string; // Comma separated emails
}

export interface CalendarTeamMember {
  userId: string;
  priority?: number;
  meetingLocationType?: 'custom' | 'zoom' | 'gmeet' | 'phone' | 'address';
  meetingLocation?: string;
  isPrimary?: boolean;
}

export interface OpenHours {
  daysOfTheWeek: number[];
  hours: {
    openHour: number;
    openMinute: number;
    closeHour: number;
    closeMinute: number;
  }[];
}

export interface Availability {
  date: string; // Format: YYYY-MM-DD in local timezone
  hours: {
    openHour: number;
    openMinute: number;
    closeHour: number;
    closeMinute: number;
  }[];
  deleted?: boolean;
  id?: string;
}

export interface LookBusyConfig {
  enabled: boolean;
  LookBusyPercentage: number;
}

// Calendar Request Types
export interface GetFreeSlotsQueryParams {
  enableLookBusy?: boolean;
  timezone?: string;
  userId?: string;
  userIds?: string[];
  startDate: number;
  endDate: number;
}

export interface UpdateCalendarRequest {
  notifications?: CalendarNotification[];
  groupId?: string;
  teamMembers?: CalendarTeamMember[];
  eventType?:
    | 'RoundRobin_OptimizeForAvailability'
    | 'RoundRobin_OptimizeForEqualDistribution';
  name: string;
  description?: string;
  slug?: string;
  widgetSlug?: string;
  widgetType?: 'default' | 'classic';
  eventTitle?: string;
  eventColor?: string;
  meetingLocation?: string;
  slotDuration?: number;
  slotDurationUnit?: 'mins' | 'hours';
  slotInterval?: number;
  slotIntervalUnit?: 'mins' | 'hours';
  slotBuffer?: number;
  slotBufferUnit?: 'mins' | 'hours';
  preBuffer?: number;
  preBufferUnit?: 'mins' | 'hours';
  appoinmentPerSlot?: number;
  appoinmentPerDay?: number;
  allowBookingAfter?: number;
  allowBookingAfterUnit?: 'hours' | 'days' | 'weeks' | 'months';
  allowBookingFor?: number;
  allowBookingForUnit?: 'days' | 'weeks' | 'months';
  openHours?: OpenHours[];
  enableRecurring?: boolean;
  recurring?: {
    freq: 'DAILY' | 'WEEKLY' | 'MONTHLY';
    count?: number;
    bookingOption?: 'skip' | 'continue' | 'book_next';
    bookingOverlapDefaultStatus?: 'confirmed' | 'new';
  };
  formId?: string;
  stickyContact?: boolean;
  isLivePaymentMode?: boolean;
  autoConfirm?: boolean;
  shouldSendAlertEmailsToAssignedMember?: boolean;
  alertEmail?: string;
  googleInvitationEmails?: boolean;
  allowReschedule?: boolean;
  allowCancellation?: boolean;
  shouldAssignContactToTeamMember?: boolean;
  shouldSkipAssigningContactForExisting?: boolean;
  notes?: string;
  pixelId?: string;
  formSubmitType?: 'RedirectURL' | 'ThankYouMessage';
  formSubmitRedirectURL?: string;
  formSubmitThanksMessage?: string;
  availabilityType?: 0 | 1;
  availabilities?: Availability[];
  guestType?: 'count_only' | 'collect_detail';
  consentLabel?: string;
  calendarCoverImage?: string;
  lookBusyConfig?: LookBusyConfig;
}

export interface CreateCalendarRequest extends UpdateCalendarRequest {
  isActive?: boolean;
  locationId: string;
  calendarType?:
    | 'round_robin'
    | 'event'
    | 'class_booking'
    | 'collective'
    | 'service_booking';
}

// Calendar Response Types
export interface Calendar {
  isActive: boolean;
  notifications?: CalendarNotification[];
  locationId: string;
  groupId?: string;
  teamMembers?: CalendarTeamMember[];
  eventType?:
    | 'RoundRobin_OptimizeForAvailability'
    | 'RoundRobin_OptimizeForEqualDistribution';
  name: string;
  description?: string;
  slug?: string;
  widgetSlug?: string;
  calendarType?:
    | 'round_robin'
    | 'event'
    | 'class_booking'
    | 'collective'
    | 'service_booking';
  widgetType?: 'default' | 'classic';
  eventTitle?: string;
  eventColor?: string;
  meetingLocation?: string;
  slotDuration?: number;
  slotDurationUnit?: 'mins' | 'hours';
  slotInterval?: number;
  slotIntervalUnit?: 'mins' | 'hours';
  slotBuffer?: number;
  slotBufferUnit?: 'mins' | 'hours';
  preBuffer?: number;
  preBufferUnit?: 'mins' | 'hours';
  appoinmentPerSlot?: number;
  appoinmentPerDay?: number;
  allowBookingAfter?: number;
  allowBookingAfterUnit?: 'hours' | 'days' | 'weeks' | 'months';
  allowBookingFor?: number;
  allowBookingForUnit?: 'days' | 'weeks' | 'months';
  openHours?: OpenHours[];
  enableRecurring?: boolean;
  recurring?: {
    freq: 'DAILY' | 'WEEKLY' | 'MONTHLY';
    count?: number;
    bookingOption?: 'skip' | 'continue' | 'book_next';
    bookingOverlapDefaultStatus?: 'confirmed' | 'new';
  };
  formId?: string;
  stickyContact?: boolean;
  isLivePaymentMode?: boolean;
  autoConfirm?: boolean;
  shouldSendAlertEmailsToAssignedMember?: boolean;
  alertEmail?: string;
  googleInvitationEmails?: boolean;
  allowReschedule?: boolean;
  allowCancellation?: boolean;
  shouldAssignContactToTeamMember?: boolean;
  shouldSkipAssigningContactForExisting?: boolean;
  notes?: string;
  pixelId?: string;
  formSubmitType?: 'RedirectURL' | 'ThankYouMessage';
  formSubmitRedirectURL?: string;
  formSubmitThanksMessage?: string;
  availabilityType?: 0 | 1;
  availabilities?: Availability[];
  guestType?: 'count_only' | 'collect_detail';
  consentLabel?: string;
  calendarCoverImage?: string;
  lookBusyConfig?: LookBusyConfig;
  id: string;
}

export interface GetCalendarsResponse {
  calendars: Calendar[];
}

export interface GetFreeSlotsResponse {
  _dates_: {
    slots: string[];
  };
}

export interface DeleteCalendarResponse {
  success: boolean;
}

export interface CreateOrUpdateCalendarResponse {
  calendar: Calendar;
}
