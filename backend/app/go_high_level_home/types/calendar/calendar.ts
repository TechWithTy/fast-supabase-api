export type Notification = {
  type: string; // Notification type (e.g., email)
  shouldSendToContact: boolean; // Should send notification to contact
  shouldSendToGuest: boolean; // Should send notification to guest
  shouldSendToUser: boolean; // Should send notification to user
  shouldSendToSelectedUsers: boolean; // Should send notification to selected users
  selectedUsers: string; // Comma-separated list of selected users
};

export type TeamMember = {
  userId: string; // User ID of the team member
  priority: number; // Priority for round-robin assignment
  meetingLocationType: string; // Type of meeting location
  meetingLocation: string; // Location of the meeting
  isPrimary: boolean; // Is the primary team member
};

export type OpenHour = {
  daysOfTheWeek: number[]; // Array of days of the week (e.g., 0 for Sunday)
  hours: Array<{
    openHour: number; // Opening hour
    openMinute: number; // Opening minute
    closeHour: number; // Closing hour
    closeMinute: number; // Closing minute
  }>;
};

export type Availability = {
  date: string; // Date for custom availability (ISO format)
  hours: Array<{
    openHour: number; // Opening hour
    openMinute: number; // Opening minute
    closeHour: number; // Closing hour
    closeMinute: number; // Closing minute
  }>;
  deleted: boolean; // Is the availability entry deleted
};

export type Recurring = {
  freq: string; // Frequency of recurrence (e.g., DAILY, WEEKLY)
  count: number; // Count of recurring events
  bookingOption: string; // Booking option (e.g., skip)
  bookingOverlapDefaultStatus: string; // Default status for booking overlap
};

export type LookBusyConfig = {
  enabled: boolean; // Is the "Look Busy" feature enabled
  LookBusyPercentage: number; // Percentage to "Look Busy"
};

export type Calendar = {
  id: string; // Calendar ID
  isActive: boolean; // Is the calendar active
  notifications: Notification[]; // Array of notifications for the calendar
  locationId: string; // Location ID
  groupId?: string; // Group ID (optional)
  teamMembers: TeamMember[]; // Array of team members
  eventType: string; // Type of event (e.g., RoundRobin_OptimizeForAvailability)
  name: string; // Name of the calendar
  description?: string; // Description of the calendar (optional)
  slug?: string; // Slug for the calendar URL (optional)
  widgetSlug?: string; // Widget slug (optional)
  calendarType: string; // Type of calendar (e.g., round_robin, class_booking)
  widgetType?: string; // Widget type (e.g., default, classic)
  eventTitle?: string; // Title of the event (default: contact name)
  eventColor?: string; // Color of the event
  meetingLocation?: string; // Location of the meeting
  slotDuration: number; // Duration of each slot (default: 30 mins)
  slotDurationUnit: string; // Unit for slot duration (mins, hours)
  slotInterval: number; // Interval between slots
  slotIntervalUnit: string; // Unit for slot interval (mins, hours)
  slotBuffer?: number; // Buffer time between slots
  slotBufferUnit?: string; // Unit for buffer time (mins, hours)
  preBuffer?: number; // Pre-buffer time before slots
  preBufferUnit?: string; // Unit for pre-buffer time (mins, hours)
  appoinmentPerSlot: number; // Number of appointments per slot
  appoinmentPerDay?: number; // Number of appointments per day (optional)
  allowBookingAfter: number; // Minimum scheduling notice for events
  allowBookingAfterUnit: string; // Unit for scheduling notice (hours, days, weeks)
  allowBookingFor: number; // Minimum number of days/weeks/months for booking events
  allowBookingForUnit: string; // Unit for booking duration (days, weeks, months)
  openHours: OpenHour[]; // Array of open hours (standard availability)
  enableRecurring: boolean; // Enable recurring appointments
  recurring?: Recurring; // Recurring details (optional)
  formId?: string; // Form ID (optional)
  stickyContact?: boolean; // Sticky contact (optional)
  isLivePaymentMode?: boolean; // Is live payment mode enabled (optional)
  autoConfirm: boolean; // Automatically confirm appointments
  shouldSendAlertEmailsToAssignedMember?: boolean; // Send alert emails to assigned members (optional)
  alertEmail?: string; // Alert email address (optional)
  googleInvitationEmails?: boolean; // Send Google invitation emails (optional)
  allowReschedule: boolean; // Allow rescheduling of events
  allowCancellation: boolean; // Allow cancellation of events
  shouldAssignContactToTeamMember?: boolean; // Assign contact to a team member (optional)
  shouldSkipAssigningContactForExisting?: boolean; // Skip assigning contact if already assigned (optional)
  notes?: string; // Notes (optional)
  pixelId?: string; // Pixel ID for tracking (optional)
  formSubmitType?: string; // Form submit type (RedirectURL, ThankYouMessage)
  formSubmitRedirectURL?: string; // Redirect URL after form submission (optional)
  formSubmitThanksMessage?: string; // Thank you message after form submission (optional)
  availabilityType?: number; // Availability type (standard or custom)
  availabilities?: Availability[]; // Array of custom availabilities (optional)
  guestType?: string; // Type of guest (e.g., count_only, collect_detail)
  consentLabel?: string; // Consent label text (optional)
  calendarCoverImage?: string; // URL of calendar cover image (optional)
  lookBusyConfig?: LookBusyConfig; // Look busy configuration (optional)
};

export type GetCalendarResponse = {
  calendar: Calendar; // The calendar object returned in the response
};

export const exampleGetCalendarResponse: GetCalendarResponse = {
  calendar: {
    id: '0TkCdp9PfvLeWKYRRvIz',
    isActive: true,
    notifications: [
      {
        type: 'email',
        shouldSendToContact: true,
        shouldSendToGuest: true,
        shouldSendToUser: true,
        shouldSendToSelectedUsers: true,
        selectedUsers: 'user1@testemail.com,user2@testemail.com'
      }
    ],
    locationId: 'ocQHyuzHvysMo5N5VsXc',
    groupId: 'BqTwX8QFwXzpegMve9EQ',
    teamMembers: [
      {
        userId: 'ocQHyuzHvysMo5N5VsXc',
        priority: 0.5,
        meetingLocationType: 'custom',
        meetingLocation: 'string',
        isPrimary: true
      }
    ],
    eventType: 'RoundRobin_OptimizeForAvailability',
    name: 'test calendar',
    description: 'this is used for testing',
    slug: 'test1',
    widgetSlug: 'test1',
    calendarType: 'round_robin',
    widgetType: 'classic',
    eventTitle: '{{contact.name}}',
    eventColor: '#039be5',
    meetingLocation: 'string',
    slotDuration: 30,
    slotDurationUnit: 'mins',
    slotInterval: 30,
    slotIntervalUnit: 'mins',
    slotBuffer: 0,
    slotBufferUnit: 'mins',
    preBuffer: 0,
    preBufferUnit: 'mins',
    appoinmentPerSlot: 1,
    appoinmentPerDay: 0,
    allowBookingAfter: 0,
    allowBookingAfterUnit: 'days',
    allowBookingFor: 0,
    allowBookingForUnit: 'days',
    openHours: [
      {
        daysOfTheWeek: [0],
        hours: [
          {
            openHour: 0,
            openMinute: 0,
            closeHour: 0,
            closeMinute: 0
          }
        ]
      }
    ],
    enableRecurring: false,
    recurring: {
      freq: 'DAILY',
      count: 24,
      bookingOption: 'skip',
      bookingOverlapDefaultStatus: 'confirmed'
    },
    formId: 'string',
    stickyContact: true,
    isLivePaymentMode: true,
    autoConfirm: true,
    shouldSendAlertEmailsToAssignedMember: true,
    alertEmail: 'string',
    googleInvitationEmails: false,
    allowReschedule: true,
    allowCancellation: true,
    shouldAssignContactToTeamMember: true,
    shouldSkipAssigningContactForExisting: true,
    notes: 'string',
    pixelId: 'string',
    formSubmitType: 'ThankYouMessage',
    formSubmitRedirectURL: 'string',
    formSubmitThanksMessage: 'string',
    availabilityType: 0,
    availabilities: [
      {
        date: '2023-09-24T00:00:00.000Z',
        hours: [
          {
            openHour: 0,
            openMinute: 0,
            closeHour: 0,
            closeMinute: 0
          }
        ],
        deleted: false
      }
    ],
    guestType: 'count_only',
    consentLabel: 'string',
    calendarCoverImage: 'https://path-to-image.com',
    lookBusyConfig: {
      enabled: true,
      LookBusyPercentage: 0
    }
  }
};
