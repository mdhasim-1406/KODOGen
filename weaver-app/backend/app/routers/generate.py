from fastapi import APIRouter, BackgroundTasks, HTTPException
from app.models.request_models import GenerateWebsiteRequest
from app.core.ai_generator import DigitalArchitectGenerator
import uuid
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/generate")
async def generate_mern_application_with_digital_architect(request: GenerateWebsiteRequest, background_tasks: BackgroundTasks):
    """
    Digital Architect Protocol - Full-Stack MERN Application Generation
    Implements Dr. Reed's hierarchical dependency management and system weaving
    """
    try:
        # Generate unique task ID
        task_id = str(uuid.uuid4())
        
        # Initialize Digital Architect Generator
        digital_architect = DigitalArchitectGenerator(
            task_id=task_id,
            prompt=request.prompt
        )
        
        # Start Digital Architect Protocol in background
        background_tasks.add_task(digital_architect.generate_mern_application)
        
        logger.info(f"Digital Architect Protocol started for task: {task_id}")
        
        return {
            "task_id": task_id,
            "status": "Digital Architect Protocol activated - MERN application weaving started",
            "message": "🏗️ Dr. Reed's Digital Architect is designing your full-stack ecosystem"
        }
        
    except Exception as e:
        logger.error(f"Error starting Digital Architect Protocol: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to start MERN generation: {str(e)}")

@router.get("/status/{task_id}")
async def get_generation_status(task_id: str):
    """
    Get AI generation status (for REST API compatibility)
    """
    # Note: Real-time status is provided via WebSocket
    # This endpoint is for fallback/polling if needed
    return {
        "task_id": task_id,
        "message": "Use WebSocket connection for real-time AI generation status"
    }