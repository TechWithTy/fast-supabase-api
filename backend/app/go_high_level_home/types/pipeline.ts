export type PipelineStage = any[]; // Assuming stages are arrays of some nested objects, could be typed further if structure is known

export type Pipeline = {
  id: string; // Pipeline ID
  name: string; // Pipeline name
  stages: PipelineStage[]; // Array of stages within the pipeline
  showInFunnel: boolean; // Whether to show the pipeline in the funnel
  showInPieChart: boolean; // Whether to show the pipeline in a pie chart
  locationId: string; // Location ID associated with the pipeline
};

export type GetPipelinesResponse = {
  pipelines: Pipeline[]; // Array of pipelines returned in the response
};

export type GetPipelinesQueryParams = {
  locationId: string; // Required location ID for querying pipelines
};

export type GetPipelinesHeaders = {
  Authorization: string; // Bearer token for authorization
  Version: string; // API version (e.g., '2021-07-28')
};

export const exampleGetPipelinesResponse: GetPipelinesResponse = {
  pipelines: [
    {
      id: 'aWdODOBVOlH1RUFKWQke',
      name: 'new pipeline',
      stages: [[]], // Empty array for stages in the example
      showInFunnel: false,
      showInPieChart: true,
      locationId: 'dsjddjkndadqaja'
    }
  ]
};
