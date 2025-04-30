import { DeepPartial } from 'react-hook-form';

// Apply DeepPartial to CreateAssistantRequest for updates
export type UpdateAssistantRequest = DeepPartial<CreateAssistantRequest>;
