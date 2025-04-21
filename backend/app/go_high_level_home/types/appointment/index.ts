// Appointment structure
export type Appointment = {
  id: string;
  calendarId: string;
  status: string;
  title: string;
  appointmentStatus: string;
  assignedUserId: string;
  notes: string;
  startTime: string;
  endTime: string;
};

// Response type for getting appointments
export type GetAppointmentsResponse = {
  events: Appointment[];
};
