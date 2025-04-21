// types/index.ts

// Common task structure
export type GhlTask = {
  id: string;
  title: string;
  body: string;
  assignedTo: string;
  dueDate: string;
  completed: boolean;
  contactId: string;
};

// Common headers structure
export type AuthHeaders = {
  Authorization: string; // Bearer token for authorization
  Version: string; // API version (e.g., '2021-07-28')
};

// Task-related request types
export type TaskRequest = {
  title: string;
  body: string;
  dueDate: string;
  completed: boolean;
  assignedTo: string;
};

export type UpdateTaskCompletedRequest = {
  completed: boolean;
};

// Response types
export type GetTasksResponse = {
  tasks: GhlTask[];
};

export type TaskResponse = {
  task: GhlTask;
};

export type UpdateTaskCompletedResponse = {
  task: GhlTask;
};

export type DeleteTaskResponse = {
  succeeded: boolean;
};

export interface GetTasksHeaders {
  Authorization: string;
  Version: string;
}
