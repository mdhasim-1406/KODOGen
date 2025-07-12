from fastapi import APIRouter, HTTPException, BackgroundTasks
import uuid
import logging
from typing import Dict

from app.core.ai_generator import DigitalArchitectGenerator
from app.core.state_tracker import state_tracker, GenerationStatus
from app.core.websocket_manager import manager

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/generate")
async def generate_website(request: Dict[str, str], background_tasks: BackgroundTasks):
    """
    Generate a new website with enhanced monitoring and validation
    """
    prompt = request.get("prompt")
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt is required")
        
    # Generate unique task ID
    task_id = str(uuid.uuid4())
    
    # Initialize state tracking
    state_tracker.initialize_generation(task_id, prompt)
    await manager.initialize_task(task_id)
    
    try:
        # Start generation in background
        background_tasks.add_task(
            handle_generation,
            task_id=task_id,
            prompt=prompt
        )
        
        return {"task_id": task_id}
        
    except Exception as e:
        logger.error(f"Failed to start generation: {e}")
        state_tracker.update_status(
            task_id,
            GenerationStatus.FAILED,
            error=str(e)
        )
        raise HTTPException(status_code=500, detail=str(e))

async def handle_generation(task_id: str, prompt: str):
    """
    Handle the website generation process with monitoring
    """
    generator = DigitalArchitectGenerator(task_id, prompt)
    
    try:
        # Update status to planning
        state_tracker.update_status(
            task_id,
            GenerationStatus.PLANNING,
            progress=10,
            current_phase="blueprint_generation"
        )
        
        # Start generation
        await generator.generate_mern_application()
        
        # Validate final state
        if not state_tracker.validate_generation(task_id):
            error_state = state_tracker.get_state(task_id)
            error_msg = error_state.get("error", "Generation validation failed")
            raise Exception(error_msg)
        
        # Update final status
        state_tracker.update_status(
            task_id,
            GenerationStatus.COMPLETED,
            progress=100,
            current_phase="completed"
        )
        
    except Exception as e:
        logger.error(f"Generation failed for task {task_id}: {e}")
        state_tracker.update_status(
            task_id,
            GenerationStatus.FAILED,
            error=str(e)
        )
        await manager.send_error(task_id, str(e))
        raise

@router.get("/status/{task_id}")
async def get_generation_status(task_id: str):
    """
    Get the current status of a generation task
    """
    state = state_tracker.get_state(task_id)
    if not state:
        raise HTTPException(status_code=404, detail="Task not found")
    return state