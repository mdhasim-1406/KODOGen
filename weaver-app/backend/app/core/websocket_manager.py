from typing import Dict, List, Optional
import json
import logging
from datetime import datetime
from fastapi import WebSocket

logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.task_status: Dict[str, dict] = {}

    async def initialize_task(self, task_id: str):
        """Initialize task status tracking"""
        self.task_status[task_id] = {
            "status": "initialized",
            "progress": 0,
            "current_step": "initialization",
            "created_at": datetime.now().isoformat(),
            "last_update": datetime.now().isoformat(),
            "error": None
        }
        logger.info(f"Task initialized: {task_id}")

    async def cleanup_task(self, task_id: str):
        """Clean up task resources"""
        if task_id in self.active_connections:
            await self.active_connections[task_id].close()
            self.disconnect(task_id)
        if task_id in self.task_status:
            del self.task_status[task_id]
        logger.info(f"Task cleaned up: {task_id}")

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
                await self.cleanup_task(task_id)

    async def send_completion(self, task_id: str, preview_url: str, download_url: str):
        """Send completion notification with preview and download URLs"""
        await self.send_message(task_id, {
            "type": "completion",
            "preview_url": preview_url,
            "download_url": download_url,
            "timestamp": datetime.now().isoformat()
        })

    async def send_error(self, task_id: str, error: str):
        """Send error message and update task status"""
        if task_id in self.task_status:
            self.task_status[task_id].update({
                "status": "error",
                "error": error,
                "last_update": datetime.now().isoformat()
            })
        await self.send_message(task_id, {
            "type": "error",
            "message": error,
            "timestamp": datetime.now().isoformat()
        })

    async def send_progress(self, task_id: str, message: str, progress: int):
        """Send AI generation progress updates"""
        if task_id in self.task_status:
            self.task_status[task_id].update({
                "status": "in_progress",
                "progress": progress,
                "current_step": message,
                "last_update": datetime.now().isoformat()
            })
        await self.send_message(task_id, {
            "type": "ai_progress",
            "message": message,
            "progress": progress,
            "timestamp": datetime.now().isoformat()
        })

    async def send_log(self, task_id: str, message: str, level: str = "info"):
        """Send AI generation log messages"""
        await self.send_message(task_id, {
            "type": "ai_log",
            "level": level,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })

# Global manager instance for use across the application
manager = ConnectionManager()