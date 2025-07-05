import axios from 'axios';
import type { GenerateWebsiteRequest, GenerateWebsiteResponse, TaskStatus } from '../types/api';

// API Configuration
const API_BASE_URL = 'http://localhost:8000';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API Functions
export const generateWebsite = async (request: GenerateWebsiteRequest): Promise<GenerateWebsiteResponse> => {
  const response = await api.post<GenerateWebsiteResponse>('/api/generate', request);
  return response.data;
};

export const getTaskStatus = async (taskId: string): Promise<TaskStatus> => {
  const response = await api.get<TaskStatus>(`/api/status/${taskId}`);
  return response.data;
};

export const getPreviewUrl = (taskId: string): string => {
  return `${API_BASE_URL}/api/preview/${taskId}/`;
};

export const getDownloadUrl = (taskId: string): string => {
  return `${API_BASE_URL}/api/download/${taskId}`;
};

export const getWebSocketUrl = (taskId: string): string => {
  return `ws://localhost:8000/ws/status/${taskId}`;
};