from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class GenerateWebsiteRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=2000, description="The prompt describing the website to generate")
    
class GenerateWebsiteResponse(BaseModel):
    task_id: str = Field(..., description="Unique identifier for the generation task")
    message: str = Field(..., description="Status message")
    websocket_url: str = Field(..., description="WebSocket URL for real-time updates")

class TaskStatus(BaseModel):
    task_id: str
    status: str
    progress: int
    current_step: str
    created_at: datetime
    
class WebSocketMessage(BaseModel):
    type: str = Field(..., description="Message type: progress, log, error, complete")
    timestamp: datetime
    
class ProgressMessage(WebSocketMessage):
    step: str
    progress: int
    detail: Optional[str] = None

class LogMessage(WebSocketMessage):
    level: str = Field(default="info", description="Log level: info, warning, error")
    message: str

class ErrorMessage(WebSocketMessage):
    message: str

class CompletionMessage(WebSocketMessage):
    preview_url: str
    download_url: str