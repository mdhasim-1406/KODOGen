// API Request/Response Types
export interface GenerateWebsiteRequest {
  prompt: string;
}

export interface GenerateWebsiteResponse {
  task_id: string;
  message: string;
  websocket_url: string;
}

export interface TaskStatus {
  task_id: string;
  status: string;
  progress: number;
  current_step: string;
  created_at: string;
}

// API Error Response
export interface ApiError {
  detail: string;
}