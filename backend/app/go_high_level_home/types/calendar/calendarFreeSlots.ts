export type FreeSlotResponse = {
  _dates_: {
    slots: string[]; // Array of available time slots (as strings, ISO date-time or other format)
  };
};

export type GetFreeSlotsQueryParams = {
  enableLookBusy?: boolean; // Optional boolean to apply the "Look Busy" feature
  timezone?: string; // Optional timezone for returning free slots
  userId?: string; // Optional user ID to filter slots for a specific user
  userIds?: string[]; // Optional array of user IDs to filter slots for specific users
  endDate: number; // Required end date (in milliseconds since epoch)
  startDate: number; // Required start date (in milliseconds since epoch)
};

export type GetFreeSlotsPathParams = {
  calendarId: string; // Required calendar ID
};

export type GetFreeSlotsHeaders = {
  Authorization: string; // Bearer token for authorization
  Version: string; // API version (e.g., '2021-04-15')
};

export const exampleGetFreeSlotsResponse: FreeSlotResponse = {
  _dates_: {
    slots: [
      '2023-09-25T16:00:00+05:30',
      '2023-09-26T14:00:00+05:30',
      '2023-09-27T10:00:00+05:30'
    ]
  }
};
