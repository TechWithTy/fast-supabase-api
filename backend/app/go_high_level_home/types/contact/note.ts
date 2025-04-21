export type ContactNote = {
  id: string; // Note ID
  body: string; // Content of the note
  userId: string; // ID of the user who added the note
  dateAdded: string; // Date when the note was added (ISO string)
  contactId: string; // ID of the contact associated with the note
};

export type GetAllNotesResponse = {
  notes: ContactNote[]; // Array of contact notes
};

export type GetAllNotesPathParams = {
  contactId: string; // Required contact ID to get notes
};

export type GetAllNotesHeaders = {
  Authorization: string; // Bearer token for authorization
  Version: string; // API version (e.g., '2021-07-28')
};

export const exampleGetAllNotesResponse: GetAllNotesResponse = {
  notes: [
    {
      id: 'HGPcayliwcdoUFzvbTok',
      body: 'lorem ipsum',
      userId: 'TUcmRxWrjqzJS8EjkxNK',
      dateAdded: '2021-07-08T12:02:11.285Z',
      contactId: 'TUcmRxWrjqzJS8EjkxNK'
    }
  ]
};
