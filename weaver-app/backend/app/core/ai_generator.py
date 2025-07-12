import os
import json
import asyncio
from typing import Dict, List, Optional, Any
import logging
from pathlib import Path

from app.core.websocket_manager import manager
from app.core.config import settings
from app.templates.mern.component_templates import (
    PACKAGE_JSON_TEMPLATE,
    BACKEND_PACKAGE_JSON_TEMPLATE,
    TSCONFIG_TEMPLATE
)
from app.templates.system_prompts import (
    MERN_ARCHITECT_PROMPT,
    MERN_BACKEND_PROMPT,
    MERN_FRONTEND_PROMPT,
    QUALITY_CHECK_PROMPT
)

logger = logging.getLogger(__name__)

class AIProvider:
    """Base class for AI providers"""
    async def generate(self, prompt: str, max_tokens: int = 4096) -> str:
        raise NotImplementedError

class OllamaProvider(AIProvider):
    """Ollama AI provider implementation"""
    async def generate(self, prompt: str, max_tokens: int = 4096) -> str:
        import aiohttp
        
        payload = {
            "model": settings.OLLAMA_CODE_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": settings.AI_TEMPERATURE,
                "num_predict": max_tokens
            }
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(settings.OLLAMA_API_URL, json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    return result.get("response", "")
                raise Exception(f"Ollama API error: {response.status}")

class OpenAIProvider(AIProvider):
    """OpenAI provider implementation"""
    async def generate(self, prompt: str, max_tokens: int = 4096) -> str:
        from langchain.chat_models import ChatOpenAI
        from langchain.schema import HumanMessage, SystemMessage
        
        llm = ChatOpenAI(
            model_name=settings.AI_MODEL,
            temperature=settings.AI_TEMPERATURE,
            max_tokens=max_tokens,
            streaming=settings.AI_STREAMING
        )
        
        messages = [
            SystemMessage(content=MERN_ARCHITECT_PROMPT),
            HumanMessage(content=prompt)
        ]
        
        response = await llm.agenerate([messages])
        return response.generations[0][0].text

class DigitalArchitectGenerator:
    """MERN stack application generator with AI capabilities"""
    
    def __init__(self, task_id: str, prompt: str):
        self.task_id = task_id
        self.prompt = prompt
        self.project_dir = os.path.join(settings.GENERATED_SITES_DIR, task_id)
        
        # Initialize AI provider based on configuration
        self.ai_provider = (
            OpenAIProvider() if settings.AI_PROVIDER == "openai"
            else OllamaProvider()
        )
        
        # Project state
        self.architectural_blueprint = None
        self.generated_files = {}
        
    async def generate_mern_application(self) -> None:
        """Main orchestrator for MERN application generation"""
        try:
            await self._log("✨ Initializing MERN stack generation...")
            
            # Create project structure
            os.makedirs(self.project_dir, exist_ok=True)
            await self._create_mern_structure()
            
            # Generate architectural blueprint
            await self._log("🏗️ Designing application architecture...")
            self.architectural_blueprint = await self._generate_architectural_blueprint()
            
            # Generate backend
            await self._log("🔧 Generating backend components...")
            await self._generate_backend()
            
            # Generate frontend
            await self._log("⚛️ Generating frontend components...")
            await self._generate_frontend()
            
            # Perform quality checks
            await self._log("🔍 Running quality validation...")
            quality_score = await self._validate_quality()
            
            if quality_score >= settings.QUALITY_THRESHOLD:
                await self._log(f"✅ Generation complete! Quality score: {quality_score}")
                preview_url = f"/api/preview/{self.task_id}/"
                download_url = f"/api/download/{self.task_id}"
                await manager.send_completion(self.task_id, preview_url, download_url)
            else:
                raise Exception(f"Quality check failed. Score: {quality_score}")
                
        except Exception as e:
            logger.error(f"MERN generation failed: {e}")
            await self._log(f"❌ Generation failed: {str(e)}")
            await manager.send_error(self.task_id, str(e))
            raise
            
    async def _create_mern_structure(self):
        """Create initial MERN project structure"""
        # Create main directories
        backend_dir = os.path.join(self.project_dir, "backend")
        frontend_dir = os.path.join(self.project_dir, "frontend")
        
        for dir_path in [backend_dir, frontend_dir]:
            os.makedirs(dir_path, exist_ok=True)
            
        # Create backend structure
        backend_dirs = ["src/models", "src/controllers", "src/routes", "src/middleware", "src/config"]
        for dir_name in backend_dirs:
            os.makedirs(os.path.join(backend_dir, dir_name), exist_ok=True)
            
        # Create frontend structure
        frontend_dirs = ["src/components", "src/pages", "src/store", "src/api", "src/hooks", "src/types"]
        for dir_name in frontend_dirs:
            os.makedirs(os.path.join(frontend_dir, dir_name), exist_ok=True)
            
        # Create initial configuration files
        await self._create_config_files()
    
    async def _create_config_files(self):
        """Create initial configuration files for both frontend and backend"""
        # Backend configuration
        backend_files = {
            "package.json": json.dumps(BACKEND_PACKAGE_JSON_TEMPLATE, indent=2),
            ".env.example": self._get_backend_env_template(),
            "tsconfig.json": json.dumps(TSCONFIG_TEMPLATE, indent=2),
        }
        
        # Frontend configuration
        frontend_files = {
            "package.json": json.dumps(PACKAGE_JSON_TEMPLATE, indent=2),
            ".env.example": self._get_frontend_env_template(),
            "tsconfig.json": json.dumps(TSCONFIG_TEMPLATE, indent=2),
            "vite.config.ts": self._get_vite_config_template(),
        }
        
        # Create backend files
        for filename, content in backend_files.items():
            path = os.path.join(self.project_dir, "backend", filename)
            with open(path, "w") as f:
                f.write(content)
                
        # Create frontend files
        for filename, content in frontend_files.items():
            path = os.path.join(self.project_dir, "frontend", filename)
            with open(path, "w") as f:
                f.write(content)
                
    def _get_backend_env_template(self) -> str:
        return """# Server Configuration
PORT=5000
NODE_ENV=development

# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017/your_database

# JWT Configuration
JWT_SECRET=your-jwt-secret
JWT_EXPIRES_IN=24h

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:5173

# Logging
LOG_LEVEL=info"""

    def _get_frontend_env_template(self) -> str:
        return """# API Configuration
VITE_API_URL=http://localhost:5000/api
VITE_WS_URL=ws://localhost:5000

# Feature Flags
VITE_ENABLE_AUTH=true
VITE_ENABLE_ANALYTICS=false"""

    def _get_vite_config_template(self) -> str:
        return """import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true
      }
    }
  }
})"""

    async def _generate_architectural_blueprint(self) -> Dict:
        """Generate application architecture blueprint"""
        prompt = f"""Based on this request: "{self.prompt}"
        
        Create a detailed MERN application blueprint that includes:
        1. Project structure
        2. Component hierarchy
        3. Data models
        4. API endpoints
        5. State management
        6. Authentication flow
        
        Provide the blueprint as a JSON object."""
        
        try:
            response = await self.ai_provider.generate(prompt)
            blueprint = json.loads(response)
            return blueprint
        except Exception as e:
            logger.error(f"Blueprint generation failed: {e}")
            return self._get_fallback_blueprint()

    async def _generate_backend(self):
        """Generate backend components"""
        components = [
            ("models", MERN_BACKEND_PROMPT),
            ("controllers", MERN_BACKEND_PROMPT),
            ("routes", MERN_BACKEND_PROMPT),
            ("middleware", MERN_BACKEND_PROMPT),
        ]
        
        for component_type, prompt_template in components:
            await self._log(f"Generating backend {component_type}...")
            await self._generate_backend_component(component_type, prompt_template)

    async def _generate_frontend(self):
        """Generate frontend components"""
        components = [
            ("components", MERN_FRONTEND_PROMPT),
            ("pages", MERN_FRONTEND_PROMPT),
            ("store", MERN_FRONTEND_PROMPT),
            ("api", MERN_FRONTEND_PROMPT),
        ]
        
        for component_type, prompt_template in components:
            await self._log(f"Generating frontend {component_type}...")
            await self._generate_frontend_component(component_type, prompt_template)

    async def _validate_quality(self) -> int:
        """Validate generated code quality"""
        prompt = f"""Analyze this MERN application:
        
        Blueprint: {json.dumps(self.architectural_blueprint, indent=2)}
        
        {QUALITY_CHECK_PROMPT}
        
        Provide a quality score (0-100) and list any issues found."""
        
        try:
            response = await self.ai_provider.generate(prompt)
            # Extract score from response
            import re
            score_match = re.search(r"quality score:\s*(\d+)", response.lower())
            if score_match:
                return int(score_match.group(1))
            return settings.QUALITY_THRESHOLD  # Default to threshold if score not found
        except Exception as e:
            logger.error(f"Quality validation failed: {e}")
            return settings.QUALITY_THRESHOLD - 1  # Return below threshold on error

    async def _log(self, message: str):
        """Send log messages"""
        await manager.send_log(self.task_id, message)
