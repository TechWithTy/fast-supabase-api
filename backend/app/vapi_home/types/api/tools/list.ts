// Reuse existing Tool type
export interface ListToolsResponse {
  tools: Tool[]; // Assuming Tool is already declared in your types
  totalCount: number;
}
