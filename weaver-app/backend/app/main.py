from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import logging
from contextlib import asynccontextmanager

from app.routers import generate, preview, websocket
from app.core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting Weaver Backend...")
    
    # Ensure generated_sites directory exists
    os.makedirs(settings.GENERATED_SITES_DIR, exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    yield
    
    # Shutdown
    logger.info("Shutting down Weaver Backend...")

app = FastAPI(
    title="Weaver Backend",
    description="AI-powered website generator backend",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(generate.router, prefix="/api", tags=["generate"])
app.include_router(preview.router, prefix="/api", tags=["preview"])
app.include_router(websocket.router, prefix="/ws", tags=["websocket"])

# Mount static files for serving generated sites
app.mount("/generated", StaticFiles(directory=settings.GENERATED_SITES_DIR), name="generated")

@app.get("/")
async def root():
    return {"message": "Weaver Backend is running", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "weaver-backend"}