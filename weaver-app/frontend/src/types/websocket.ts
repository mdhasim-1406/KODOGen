// WebSocket Message Types
export interface WebSocketMessage {
  type: 'progress' | 'log' | 'error' | 'complete';
  timestamp: string;
}

export interface ProgressMessage extends WebSocketMessage {
  type: 'progress';
  step: string;
  progress: number;
  detail?: string;
}

export interface LogMessage extends WebSocketMessage {
  type: 'log';
  level: 'info' | 'warning' | 'error';
  message: string;
}

export interface ErrorMessage extends WebSocketMessage {
  type: 'error';
  message: string;
}

export interface CompletionMessage extends WebSocketMessage {
  type: 'complete';
  preview_url: string;
  download_url: string;
}

export type AnyWebSocketMessage = ProgressMessage | LogMessage | ErrorMessage | CompletionMessage;