from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import os
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List
from contextlib import asynccontextmanager
import asyncio

from app.routers import generate, preview, websocket
from app.core.config import settings
from app.core.ai_generator import DigitalArchitectGenerator

# Configure logging with more detail
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/weaver.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Global state tracking
GENERATION_STATES: Dict[str, Dict] = {}
SYSTEM_METRICS = {
    "total_generations": 0,
    "successful_generations": 0,
    "failed_generations": 0,
    "start_time": None,
    "last_health_check": None,
    "active_generations": 0
}

async def monitor_generation_health():
    """Background task to monitor generation health and cleanup stale tasks"""
    while True:
        try:
            current_time = datetime.now()
            stale_threshold = current_time - timedelta(minutes=10)
            
            # Check for stale generations
            for task_id, state in list(GENERATION_STATES.items()):
                if state["start_time"] < stale_threshold and state["status"] not in ["completed", "failed"]:
                    logger.warning(f"Stale generation detected: {task_id}")
                    GENERATION_STATES[task_id]["status"] = "failed"
                    GENERATION_STATES[task_id]["error"] = "Generation timeout"
                    SYSTEM_METRICS["failed_generations"] += 1
            
            # Update system metrics
            SYSTEM_METRICS["last_health_check"] = current_time
            SYSTEM_METRICS["active_generations"] = len([
                s for s in GENERATION_STATES.values()
                if s["status"] not in ["completed", "failed"]
            ])
            
            # Cleanup old completed tasks
            cleanup_threshold = current_time - timedelta(hours=24)
            GENERATION_STATES.clear()
            
        except Exception as e:
            logger.error(f"Error in health monitor: {e}")
        
        await asyncio.sleep(60)  # Run every minute

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting Weaver Backend...")
    SYSTEM_METRICS["start_time"] = datetime.now()
    
    # Ensure directories exist
    os.makedirs(settings.GENERATED_SITES_DIR, exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    # Start background tasks
    task = asyncio.create_task(monitor_generation_health())
    
    yield
    
    # Cleanup on shutdown
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass
    
    logger.info("Shutting down Weaver Backend...")

app = FastAPI(
    title="Weaver Backend",
    description="AI-powered website generator backend",
    version="1.0.0",
    lifespan=lifespan
)

# Rate limiting middleware
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    # Basic rate limiting
    client_ip = request.client.host
    current_time = time.time()
    
    # Allow 60 requests per minute per IP
    if hasattr(app.state, 'rate_limit'):
        if client_ip in app.state.rate_limit:
            requests = [t for t in app.state.rate_limit[client_ip] if current_time - t < 60]
            if len(requests) >= 60:
                return JSONResponse(
                    status_code=429,
                    content={"detail": "Too many requests"}
                )
            app.state.rate_limit[client_ip] = requests + [current_time]
        else:
            app.state.rate_limit[client_ip] = [current_time]
    else:
        app.state.rate_limit = {client_ip: [current_time]}
    
    response = await call_next(request)
    return response

# Error handling middleware
@app.middleware("http")
async def error_handling_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logger.error(f"Unhandled error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=eval(settings.CORS_ORIGINS),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "uptime": str(datetime.now() - SYSTEM_METRICS["start_time"]),
        "metrics": {
            "total_generations": SYSTEM_METRICS["total_generations"],
            "successful_generations": SYSTEM_METRICS["successful_generations"],
            "failed_generations": SYSTEM_METRICS["failed_generations"],
            "active_generations": SYSTEM_METRICS["active_generations"]
        },
        "last_health_check": SYSTEM_METRICS["last_health_check"].isoformat() if SYSTEM_METRICS["last_health_check"] else None
    }

# Generation status endpoint
@app.get("/api/status/{task_id}")
async def get_generation_status(task_id: str):
    if task_id not in GENERATION_STATES:
        raise HTTPException(status_code=404, content={"detail": "Generation task not found"})
    return GENERATION_STATES[task_id]

# Include routers
app.include_router(generate.router, prefix="/api", tags=["generate"])
app.include_router(preview.router, prefix="/api", tags=["preview"])
app.include_router(websocket.router, prefix="/ws", tags=["websocket"])

# Mount static files for serving generated sites
app.mount("/sites", StaticFiles(directory=settings.GENERATED_SITES_DIR), name="sites")