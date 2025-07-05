from typing import Dict, List
import json
import logging
from fastapi import WebSocket

logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, task_id: str):
        await websocket.accept()
        self.active_connections[task_id] = websocket
        logger.info(f"WebSocket connected for task: {task_id}")

    def disconnect(self, task_id: str):
        if task_id in self.active_connections:
            del self.active_connections[task_id]
            logger.info(f"WebSocket disconnected for task: {task_id}")

    async def send_message(self, task_id: str, message: dict):
        if task_id in self.active_connections:
            try:
                await self.active_connections[task_id].send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"Error sending message to {task_id}: {e}")
                self.disconnect(task_id)

    # Enhanced methods for AI streaming
    async def send_progress(self, task_id: str, message: str, progress: int):
        """Send AI generation progress updates"""
        await self.send_message(task_id, {
            "type": "ai_progress",
            "message": message,
            "progress": progress,
            "timestamp": json.dumps({"$date": {"$numberLong": str(int(1000 * 1000000))}})
        })

    async def send_log(self, task_id: str, message: str):
        """Send AI generation log messages"""
        await self.send_message(task_id, {
            "type": "ai_log",
            "message": message,
            "timestamp": json.dumps({"$date": {"$numberLong": str(int(1000 * 1000000))}})
        })

    async def send_code_chunk(self, task_id: str, content: str):
        """Stream AI-generated code chunks in real-time"""
        await self.send_message(task_id, {
            "type": "ai_code_chunk",
            "content": content,
            "timestamp": json.dumps({"$date": {"$numberLong": str(int(1000 * 1000000))}})
        })

    async def send_ai_phase(self, task_id: str, phase: str, message: str, progress: int):
        """Send AI generation phase updates"""
        await self.send_message(task_id, {
            "type": "ai_phase",
            "phase": phase,
            "message": message,
            "progress": progress,
            "timestamp": json.dumps({"$date": {"$numberLong": str(int(1000 * 1000000))}})
        })

    async def send_completion(self, task_id: str, preview_url: str, download_url: str):
        """Send AI generation completion notification"""
        await self.send_message(task_id, {
            "type": "ai_complete",
            "preview_url": preview_url,
            "download_url": download_url,
            "message": "🎉 AI generation complete! Your website is ready!",
            "timestamp": json.dumps({"$date": {"$numberLong": str(int(1000 * 1000000))}})
        })

    async def send_error(self, task_id: str, error_message: str):
        """Send AI generation error notification"""
        await self.send_message(task_id, {
            "type": "ai_error",
            "message": error_message,
            "timestamp": json.dumps({"$date": {"$numberLong": str(int(1000 * 1000000))}})
        })

# Global manager instance for use across the application
manager = ConnectionManager()