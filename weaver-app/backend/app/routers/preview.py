from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
import logging

from app.core.website_generator import WebsiteGenerator
from app.core.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/preview/{task_id}/")
async def preview_website_root(task_id: str):
    """Serve the index.html of the generated website"""
    project_dir = os.path.join(settings.GENERATED_SITES_DIR, task_id)
    index_path = os.path.join(project_dir, "index.html")
    
    if not os.path.exists(index_path):
        raise HTTPException(status_code=404, detail="Generated website not found")
    
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    return HTMLResponse(content=content)

@router.get("/preview/{task_id}/{file_path:path}")
async def preview_website_file(task_id: str, file_path: str):
    """Serve static files from the generated website"""
    project_dir = os.path.join(settings.GENERATED_SITES_DIR, task_id)
    full_path = os.path.join(project_dir, file_path)
    
    # Security check - ensure the file is within the project directory
    if not full_path.startswith(project_dir):
        raise HTTPException(status_code=403, detail="Access denied")
    
    if not os.path.exists(full_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(full_path)

@router.get("/download/{task_id}")
async def download_website(task_id: str):
    """Download the generated website as a ZIP file"""
    project_dir = os.path.join(settings.GENERATED_SITES_DIR, task_id)
    
    if not os.path.exists(project_dir):
        raise HTTPException(status_code=404, detail="Generated website not found")
    
    try:
        # Create a temporary generator instance to create the ZIP
        generator = WebsiteGenerator(task_id, "")
        zip_path = generator.create_zip_archive()
        
        if not os.path.exists(zip_path):
            raise HTTPException(status_code=500, detail="Failed to create ZIP archive")
        
        return FileResponse(
            zip_path,
            media_type='application/zip',
            filename=f"website_{task_id}.zip"
        )
        
    except Exception as e:
        logger.error(f"Error creating ZIP for task {task_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to create download archive")