export type ContactAppointment = {
  id: string; // Appointment ID
  calendarId: string; // Calendar ID associated with the appointment
  status: string; // Status of the appointment (e.g., "booked", "canceled")
  title: string; // Title of the appointment
  appointmentStatus: string; // Detailed status (e.g., "confirmed", "pending")
  assignedUserId: string; // ID of the user assigned to the appointment
  notes?: string; // Optional notes about the appointment
  startTime: string; // Start time of the appointment (ISO string or date-time string)
  endTime: string; // End time of the appointment (ISO string or date-time string)
};

export type GetAppointmentsForContactResponse = {
  events: ContactAppointment[]; // Array of appointments (events)
};

export type GetAppointmentsForContactPathParams = {
  contactId: string; // Required contact ID to get appointments
};

export type GetAppointmentsForContactHeaders = {
  Authorization: string; // Bearer token for authorization
  Version: string; // API version (e.g., '2021-07-28')
};
export const exampleGetAppointmentsForContactResponse: GetAppointmentsForContactResponse =
  {
    events: [
      {
        id: 'YS3jaqqeehkR2Is80miy',
        calendarId: 'YlWd2wuCAZQzh2cH1fVZ',
        status: 'booked',
        title: 'Test',
        appointmentStatus: 'confirmed',
        assignedUserId: 'YlWd2wuCAZQzh2cH1fVZ',
        notes: 'test',
        startTime: '2021-07-16 11:00:00',
        endTime: '2021-07-16 11:30:00'
      }
    ]
  };
