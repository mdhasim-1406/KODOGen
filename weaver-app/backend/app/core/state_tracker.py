"""
Generation State Tracker
Monitors and validates the generation process
"""

import logging
from typing import Dict, Optional
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)

class GenerationStatus(Enum):
    INITIALIZED = "initialized"
    PLANNING = "planning"
    GENERATING_BACKEND = "generating_backend"
    GENERATING_FRONTEND = "generating_frontend"
    ANALYZING = "analyzing"
    REFINING = "refining"
    COMPLETED = "completed"
    FAILED = "failed"

class GenerationStateTracker:
    def __init__(self):
        self.states: Dict[str, Dict] = {}
    
    def initialize_generation(self, task_id: str, prompt: str) -> None:
        """Initialize a new generation task"""
        self.states[task_id] = {
            "task_id": task_id,
            "prompt": prompt,
            "status": GenerationStatus.INITIALIZED.value,
            "start_time": datetime.now(),
            "last_update": datetime.now(),
            "progress": 0,
            "files_generated": 0,
            "total_files": 0,
            "current_phase": "initialization",
            "error": None,
            "quality_metrics": {
                "blueprint_quality": None,
                "code_quality": None,
                "interconnection_score": None
            }
        }
        logger.info(f"Generation initialized: {task_id}")
    
    def update_status(
        self, 
        task_id: str, 
        status: GenerationStatus,
        progress: Optional[int] = None,
        current_phase: Optional[str] = None,
        files_generated: Optional[int] = None,
        error: Optional[str] = None
    ) -> None:
        """Update the status of a generation task"""
        if task_id not in self.states:
            logger.error(f"Task {task_id} not found")
            return
        
        state = self.states[task_id]
        state["status"] = status.value
        state["last_update"] = datetime.now()
        
        if progress is not None:
            state["progress"] = progress
        if current_phase is not None:
            state["current_phase"] = current_phase
        if files_generated is not None:
            state["files_generated"] = files_generated
        if error is not None:
            state["error"] = error
            
        logger.info(f"Generation status updated: {task_id} -> {status.value}")
    
    def update_quality_metrics(
        self,
        task_id: str,
        blueprint_quality: Optional[float] = None,
        code_quality: Optional[float] = None,
        interconnection_score: Optional[float] = None
    ) -> None:
        """Update quality metrics for a generation task"""
        if task_id not in self.states:
            logger.error(f"Task {task_id} not found")
            return
            
        metrics = self.states[task_id]["quality_metrics"]
        if blueprint_quality is not None:
            metrics["blueprint_quality"] = blueprint_quality
        if code_quality is not None:
            metrics["code_quality"] = code_quality
        if interconnection_score is not None:
            metrics["interconnection_score"] = interconnection_score
    
    def get_state(self, task_id: str) -> Optional[Dict]:
        """Get the current state of a generation task"""
        return self.states.get(task_id)
    
    def validate_generation(self, task_id: str) -> bool:
        """Validate the generation process"""
        if task_id not in self.states:
            return False
            
        state = self.states[task_id]
        
        # Check for timeouts
        if (datetime.now() - state["start_time"]).total_seconds() > 600:  # 10 minutes
            self.update_status(
                task_id,
                GenerationStatus.FAILED,
                error="Generation timeout"
            )
            return False
        
        # Check for progress stalls
        if (datetime.now() - state["last_update"]).total_seconds() > 120:  # 2 minutes
            self.update_status(
                task_id,
                GenerationStatus.FAILED,
                error="Generation stalled"
            )
            return False
        
        # Validate quality metrics if complete
        if state["status"] == GenerationStatus.COMPLETED.value:
            metrics = state["quality_metrics"]
            if not all(metrics.values()):
                self.update_status(
                    task_id,
                    GenerationStatus.FAILED,
                    error="Incomplete quality metrics"
                )
                return False
            
            # Check if quality scores are acceptable
            if (metrics["blueprint_quality"] < 0.7 or
                metrics["code_quality"] < 0.7 or
                metrics["interconnection_score"] < 0.7):
                self.update_status(
                    task_id,
                    GenerationStatus.FAILED,
                    error="Quality standards not met"
                )
                return False
        
        return True
    
    def cleanup_old_states(self, hours: int = 24) -> None:
        """Clean up old generation states"""
        current_time = datetime.now()
        self.states = {
            task_id: state
            for task_id, state in self.states.items()
            if (current_time - state["start_time"]).total_seconds() < hours * 3600
        }

# Global state tracker instance
state_tracker = GenerationStateTracker()
