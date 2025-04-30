import { ToolMessage } from '../calls/create';
import { ToolType } from './create';

export interface GetToolResponse {
  async: boolean;
  messages: ToolMessage[];
  type: ToolType;
  id: string;
  orgId: string;
  createdAt: string;
  updatedAt: string;
  function: {
    name: string;
    description: string;
    parameters: {
      type: 'object';
      properties: Record<string, any>;
      required: string[];
    };
  };
  server: {
    timeoutSeconds: number;
    url: string;
    secret: string;
  };
}
