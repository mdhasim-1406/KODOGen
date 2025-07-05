from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import logging

from app.core.websocket_manager import manager

router = APIRouter()
logger = logging.getLogger(__name__)

@router.websocket("/status/{task_id}")
async def websocket_status(websocket: WebSocket, task_id: str):
    """WebSocket endpoint for real-time task status updates"""
    await manager.connect(websocket, task_id)
    
    try:
        # Send initial connection confirmation
        await manager.send_log(task_id, f"Connected to task {task_id} status stream", "info")
        
        # Keep connection alive and handle incoming messages
        while True:
            try:
                # Wait for any client messages (like ping/pong for keepalive)
                data = await websocket.receive_text()
                logger.debug(f"Received WebSocket message for task {task_id}: {data}")
                
                # Echo back any ping messages
                if data == "ping":
                    await websocket.send_text("pong")
                    
            except WebSocketDisconnect:
                break
            except Exception as e:
                logger.error(f"WebSocket error for task {task_id}: {e}")
                break
                
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for task {task_id}")
    except Exception as e:
        logger.error(f"WebSocket connection error for task {task_id}: {e}")
    finally:
        manager.disconnect(websocket, task_id)