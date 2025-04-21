export interface DeleteToolResponse {
  id: string; // Unique identifier of the deleted tool
  status: 'deleted'; // Status indicating successful deletion
  orgId: string; // Organization ID associated with the tool
  deletedAt: string; // ISO timestamp of when the tool was deleted
}
