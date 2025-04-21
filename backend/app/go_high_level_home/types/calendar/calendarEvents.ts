export type CalendarEvent = {
  id: string; // Event ID
  address?: string; // Optional address (e.g., Google Meet URL)
  title: string; // Event title
  calendarId: string; // Calendar ID the event belongs to
  locationId: string; // Location ID
  contactId: string; // Contact ID
  groupId: string; // Group ID
  appointmentStatus: string; // Status of the appointment (e.g., confirmed)
  assignedUserId: string; // User ID of the primary owner of the appointment
  users: string[]; // Array of secondary owners' User IDs
  notes?: string; // Optional notes for the event
  startTime: string; // Start time of the event (ISO string)
  endTime: string; // End time of the event (ISO string)
  dateAdded: string; // Date the event was added (ISO string)
  dateUpdated: string; // Date the event was last updated (ISO string)
  assignedResources?: string[]; // Optional array of IDs for associated resources (rooms/equipment)
};

export type GetCalendarEventsResponse = {
  events: CalendarEvent[]; // Array of calendar events
};

export const exampleGetCalendarEventsResponse: GetCalendarEventsResponse = {
  events: [
    {
      id: '0007BWpSzSwfiuSl0tR2',
      address: 'https://meet.google.com/yqp-gogr-wve',
      title: 'Appointment with GHL Dev team',
      calendarId: 'BqTwX8QFwXzpegMve9EQ',
      locationId: '0007BWpSzSwfiuSl0tR2',
      contactId: '9NkT25Vor1v4aQatFsv2',
      groupId: '9NkT25Vor1v4aQatFsv2',
      appointmentStatus: 'confirmed',
      assignedUserId: 'YlWd2wuCAZQzh2cH1fVZ',
      users: ['YlWd2wuCAZQzh2cH1fVZ', '9NkT25Vor1v4aQatFsv2'],
      notes: 'Some dummy note',
      startTime: '2023-09-25T16:00:00+05:30',
      endTime: '2023-09-25T16:00:00+05:30',
      dateAdded: '2023-09-25T16:00:00+05:30',
      dateUpdated: '2023-09-25T16:00:00+05:30',
      assignedResources: ['string']
    }
  ]
};
