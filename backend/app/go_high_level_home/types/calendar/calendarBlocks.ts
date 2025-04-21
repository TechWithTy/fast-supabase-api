export type BlockedSlotEvent = {
  id: string; // Calendar Event ID
  address?: string; // Optional event address (e.g., a URL for a video call)
  title: string; // Event title (e.g., Appointment name)
  calendarId: string; // Calendar ID the event belongs to
  locationId: string; // Location ID
  contactId: string; // Contact ID associated with the event
  groupId: string; // Group ID for the event
  appointmentStatus: string; // Status of the appointment (e.g., confirmed, canceled)
  assignedUserId: string; // ID of the primary owner of the appointment
  users: string[]; // Array of secondary user IDs
  notes?: string; // Optional notes for the event
  startTime: string; // Start time of the event (ISO string)
  endTime: string; // End time of the event (ISO string)
  dateAdded: string; // Date when the event was added (ISO string)
  dateUpdated: string; // Date when the event was last updated (ISO string)
  assignedResources?: string[]; // Optional array of resource IDs (e.g., rooms or equipment)
};

export type GetBlockedSlotsResponse = {
  events: BlockedSlotEvent[]; // Array of blocked slots (calendar events)
};

export const exampleGetBlockedSlotsResponse: GetBlockedSlotsResponse = {
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
