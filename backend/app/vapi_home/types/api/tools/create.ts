import { ToolMessage } from '../calls/create';

// Define the enums for ToolType and Operator
export enum ToolType {
  DTMF = 'DtmfTool',
  EndCall = 'EndCallTool',
  Function = 'FunctionTool',
  Ghl = 'GhlTool',
  Make = 'MakeTool',
  TransferCall = 'TransferCallTool',
  Output = 'OutputTool'
}

export enum ConditionOperator {
  Equals = 'eq',
  NotEquals = 'ne',
  GreaterThan = 'gt',
  LessThan = 'lt'
}

export interface CreateToolRequest {
  async: boolean;
  messages: ToolMessage[];
  type: ToolType;
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

export interface CreateToolResponse {
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
