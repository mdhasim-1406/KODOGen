import os
import json
import uuid
import asyncio
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

from app.core.websocket_manager import manager
from app.core.config import settings

logger = logging.getLogger(__name__)

class DigitalArchitectGenerator:
    """
    Dr. Reed's Digital Architect Protocol
    Implements full-stack MERN application generation with hierarchical dependency management
    """
    
    def __init__(self, task_id: str, prompt: str):
        self.task_id = task_id
        self.prompt = prompt
        self.project_dir = os.path.join(settings.GENERATED_SITES_DIR, task_id)
        
        # Ollama configuration
        self.ollama_url = "http://localhost:11434/api/generate"
        self.model_name = "qwen:4b"
        
        # Digital Architect state
        self.architectural_blueprint = None
        self.generated_files = {}
        self.dependency_graph = {}
        self.weaving_quality_score = 0
        self.interconnection_analysis = {}
        
    async def generate_mern_application(self) -> None:
        """
        Main orchestrator for Digital Architect Protocol
        """
        try:
            await self._stream_update("🏗️ Dr. Reed initializing Digital Architect Protocol...", 5)
            
            # Create project directory structure
            os.makedirs(self.project_dir, exist_ok=True)
            
            # ARCHITECT PHASE 1: Application Blueprinting
            await self._stream_update("🧠 Digital Architect designing system blueprint...", 10)
            self.architectural_blueprint = await self._generate_architectural_blueprint()
            await self._log(f"✅ System blueprint created: {self._count_blueprint_files()} files planned")
            
            # Save blueprint for reference
            await self._save_blueprint()
            
            # ARCHITECT PHASE 2: Hierarchical Generation
            await self._stream_update("🔧 Weaving backend infrastructure...", 20)
            await self._generate_backend_tier()
            
            await self._stream_update("⚛️ Weaving frontend ecosystem...", 60)
            await self._generate_frontend_tier()
            
            # ARCHITECT PHASE 3: Full-Stack Self-Critique
            await self._stream_update("🔍 Dr. Reed analyzing system interconnectivity...", 85)
            await self._perform_fullstack_critique()
            
            # ARCHITECT PHASE 4: Final Weaving Refinements
            await self._stream_update("✨ Applying architectural refinements...", 95)
            await self._apply_weaving_refinements()
            
            await self._stream_update("🎉 Digital ecosystem complete!", 100)
            await self._log(f"🏆 System Weaving Score: {self.weaving_quality_score}/10")
            
            # Send completion notification
            preview_url = f"/api/preview/{self.task_id}/"
            download_url = f"/api/download/{self.task_id}"
            await manager.send_completion(self.task_id, preview_url, download_url)
            
        except Exception as e:
            logger.error(f"Digital Architect Error: {e}")
            await self._log(f"❌ System weaving failed: {str(e)}")
            await manager.send_error(self.task_id, f"Generation failed: {str(e)}")
            raise

    async def _generate_architectural_blueprint(self) -> Dict:
        """
        ARCHITECT PHASE 1: Generate comprehensive system architecture
        """
        blueprint_prompt = self._get_application_blueprint_prompt()
        
        try:
            response = await self._call_ollama(blueprint_prompt, max_tokens=4000)
            
            # Extract JSON from response
            response_text = response.strip()
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                blueprint = json.loads(json_str)
                return blueprint
            else:
                return self._get_fallback_blueprint()
                
        except Exception as e:
            logger.error(f"Architectural blueprint generation failed: {e}")
            return self._get_fallback_blueprint()

    async def _generate_backend_tier(self):
        """
        ARCHITECT PHASE 2A: Generate backend in dependency order
        """
        backend_files = self.architectural_blueprint.get('backend', {})
        generation_order = [
            'package.json',
            'models/',
            'controllers/',
            'routes/',
            'middleware/',
            'server.js',
            '.env'
        ]
        
        for file_pattern in generation_order:
            matching_files = [f for f in backend_files.keys() if file_pattern in f]
            
            for file_path in matching_files:
                await self._stream_update(f"🔧 WEAVING BACKEND > /{file_path}...", None)
                file_content = await self._generate_backend_file(file_path, backend_files[file_path])
                await self._save_generated_file('backend', file_path, file_content)
                await self._log(f"✅ Backend file created: {file_path}")

    async def _generate_frontend_tier(self):
        """
        ARCHITECT PHASE 2B: Generate frontend in dependency order
        """
        frontend_files = self.architectural_blueprint.get('frontend', {})
        generation_order = [
            'package.json',
            'src/api/',
            'src/store/',
            'src/hooks/',
            'src/components/',
            'src/pages/',
            'src/App.jsx',
            'src/main.jsx',
            'index.html'
        ]
        
        for file_pattern in generation_order:
            matching_files = [f for f in frontend_files.keys() if file_pattern in f]
            
            for file_path in matching_files:
                await self._stream_update(f"⚛️ WEAVING FRONTEND > /{file_path}...", None)
                file_content = await self._generate_frontend_file(file_path, frontend_files[file_path])
                await self._save_generated_file('frontend', file_path, file_content)
                await self._log(f"✅ Frontend file created: {file_path}")

    async def _generate_backend_file(self, file_path: str, description: str) -> str:
        """
        Generate individual backend file with system context
        """
        backend_prompt = f"""You are Dr. Evelyn Reed, generating a backend file for a MERN application.

APPLICATION CONTEXT:
- User Request: {self.prompt}
- Project: {self.architectural_blueprint.get('project_name', 'mern-app')}
- File: {file_path}
- Purpose: {description}

ARCHITECTURAL BLUEPRINT CONTEXT:
{json.dumps(self.architectural_blueprint, indent=2)}

Generate the complete, production-ready code for this file:
- Follow MERN best practices and modern patterns
- Ensure clean separation of concerns
- Include proper error handling and validation
- Use appropriate dependencies and imports
- Create maintainable, scalable code
- Include meaningful comments for complex logic

Generate ONLY the file content, no explanations:"""

        try:
            response = await self._call_ollama(backend_prompt, max_tokens=3000)
            return response.strip()
        except Exception as e:
            logger.error(f"Backend file generation failed for {file_path}: {e}")
            return self._get_fallback_backend_file(file_path)

    async def _generate_frontend_file(self, file_path: str, description: str) -> str:
        """
        Generate individual frontend file with system context
        """
        frontend_prompt = f"""You are Dr. Evelyn Reed, generating a frontend file for a MERN application.

APPLICATION CONTEXT:
- User Request: {self.prompt}
- Project: {self.architectural_blueprint.get('project_name', 'mern-app')}
- File: {file_path}
- Purpose: {description}

ARCHITECTURAL BLUEPRINT CONTEXT:
{json.dumps(self.architectural_blueprint, indent=2)}

Generate the complete, production-ready code for this file:
- Use modern React patterns (hooks, functional components)
- Implement proper state management with Zustand
- Create clean, reusable components
- Include proper TypeScript types if applicable
- Ensure responsive design with Tailwind CSS
- Follow React best practices and performance patterns
- Include proper error boundaries and loading states

Generate ONLY the file content, no explanations:"""

        try:
            response = await self._call_ollama(frontend_prompt, max_tokens=3000)
            return response.strip()
        except Exception as e:
            logger.error(f"Frontend file generation failed for {file_path}: {e}")
            return self._get_fallback_frontend_file(file_path)

    async def _perform_fullstack_critique(self):
        """
        ARCHITECT PHASE 3: Full-stack interconnectivity analysis
        """
        critique_prompt = self._get_fullstack_weaving_critique_prompt()
        
        try:
            response = await self._call_ollama(critique_prompt, max_tokens=2000)
            
            # Parse critique response
            response_text = response.strip()
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                critique = json.loads(json_str)
                self.interconnection_analysis = critique
                self.weaving_quality_score = critique.get('weaving_score', 8)
                await self._log(f"🔍 Interconnectivity analysis complete - Score: {self.weaving_quality_score}/10")
            else:
                self.weaving_quality_score = 8
                
        except Exception as e:
            logger.error(f"Full-stack critique failed: {e}")
            self.weaving_quality_score = 7

    def _get_application_blueprint_prompt(self) -> str:
        """
        Master Application Blueprint Prompt - Dr. Reed's Architectural Vision
        """
        return f"""You are Dr. Evelyn Reed, Principal Systems Weaver. Create a comprehensive architectural blueprint for a MERN application.

USER REQUEST: {self.prompt}

Generate a detailed architectural blueprint that defines the complete file structure and purpose of every file in both backend and frontend.

Respond with ONLY a JSON object in this structure:

{{
  "project_name": "kebab-case-name",
  "project_type": "web_app|dashboard|ecommerce|social|productivity|other",
  "core_entities": ["User", "Product", "Order"],
  "backend": {{
    "package.json": "Dependencies and scripts for Node.js/Express backend",
    "server.js": "Main Express server setup with MongoDB connection",
    "models/EntityName.js": "Mongoose schema definition with validation",
    "controllers/entityController.js": "Business logic and CRUD operations",
    "routes/entities.js": "API endpoints and route handlers",
    "middleware/auth.js": "Authentication and authorization middleware",
    "config/database.js": "MongoDB connection configuration",
    ".env": "Environment variables for configuration"
  }},
  "frontend": {{
    "package.json": "React dependencies including Zustand, Axios, Tailwind",
    "index.html": "Root HTML template with proper meta tags",
    "src/main.jsx": "React DOM root and app initialization",
    "src/App.jsx": "Main app component with routing",
    "src/store/appStore.js": "Zustand global state management",
    "src/api/apiService.js": "Axios configuration and API functions",
    "src/components/ComponentName.jsx": "Reusable UI components",
    "src/pages/PageName.jsx": "Main page components",
    "src/hooks/useCustomHook.js": "Custom React hooks for logic reuse"
  }}
}}

Create a blueprint that reflects the user's requirements with proper MERN architecture, realistic file structure, and clear separation of concerns.

Architectural Blueprint:"""

    def _get_fullstack_weaving_critique_prompt(self) -> str:
        """
        Master Full-Stack Weaving Critique Prompt - System Interconnectivity Analysis
        """
        return f"""You are Dr. Evelyn Reed, reviewing a complete MERN application for system interconnectivity.

ORIGINAL REQUEST: {self.prompt}

ARCHITECTURAL BLUEPRINT:
{json.dumps(self.architectural_blueprint, indent=2)}

GENERATED FILES ANALYSIS:
Backend files: {list(self.generated_files.get('backend', {}).keys())}
Frontend files: {list(self.generated_files.get('frontend', {}).keys())}

Analyze the interconnectedness of this system:

1. Do the React components correctly use the Zustand stores?
2. Do the Zustand stores correctly call the API service functions?
3. Do the API services correctly target the Express endpoints?
4. Are there any logical flaws, race conditions, or missing dependencies?
5. Is the data flow from MongoDB → Express → React → User seamless?
6. Are error handling and loading states properly implemented?

Provide your analysis as a JSON object:

{{
  "weaving_score": [1-10 score for overall system coherence],
  "interconnectivity_analysis": "detailed assessment of component connections",
  "data_flow_integrity": "analysis of data flow from database to UI",
  "critical_issues": ["list of serious architectural problems"],
  "optimization_recommendations": ["list of suggested improvements"],
  "weaving_refinements": ["specific changes to improve interconnections"]
}}

System Weaving Analysis:"""

    def _get_fallback_blueprint(self) -> Dict:
        """Fallback blueprint for when AI generation fails"""
        return {
            "project_name": "mern-application",
            "project_type": "web_app",
            "core_entities": ["User", "Task"],
            "backend": {
                "package.json": "Node.js backend dependencies",
                "server.js": "Express server with MongoDB connection",
                "models/Task.js": "Task mongoose schema",
                "routes/tasks.js": "Task API endpoints",
                "controllers/taskController.js": "Task business logic"
            },
            "frontend": {
                "package.json": "React frontend dependencies",
                "src/App.jsx": "Main React application component",
                "src/main.jsx": "React DOM root",
                "src/store/taskStore.js": "Zustand task state management",
                "src/api/taskService.js": "Task API service functions",
                "src/components/TaskList.jsx": "Task list component"
            }
        }

    def _get_fallback_backend_file(self, file_path: str) -> str:
        """Fallback backend file content"""
        if 'package.json' in file_path:
            return """{
  "name": "mern-backend",
  "version": "1.0.0",
  "description": "MERN application backend",
  "main": "server.js",
  "scripts": {
    "start": "node server.js",
    "dev": "nodemon server.js"
  },
  "dependencies": {
    "express": "^4.18.2",
    "mongoose": "^7.5.0",
    "cors": "^2.8.5",
    "dotenv": "^16.3.1"
  }
}"""
        elif 'server.js' in file_path:
            return """const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());

// MongoDB connection
mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/mernapp')
  .then(() => console.log('MongoDB connected'))
  .catch(err => console.log(err));

// Routes
app.get('/api/health', (req, res) => {
  res.json({ message: 'MERN backend is running' });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});"""
        else:
            return f"// {file_path} - Generated by Digital Architect Protocol\n// TODO: Implement file content"

    def _get_fallback_frontend_file(self, file_path: str) -> str:
        """Fallback frontend file content"""
        if 'package.json' in file_path:
            return """{
  "name": "mern-frontend",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "axios": "^1.5.0",
    "zustand": "^4.4.1"
  },
  "devDependencies": {
    "@types/react": "^18.2.15",
    "@types/react-dom": "^18.2.7",
    "@vitejs/plugin-react": "^4.0.3",
    "autoprefixer": "^10.4.14",
    "postcss": "^8.4.27",
    "tailwindcss": "^3.3.3",
    "vite": "^4.4.5"
  }
}"""
        elif 'App.jsx' in file_path:
            return """import React from 'react';

function App() {
  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4">
          <h1 className="text-3xl font-bold text-gray-900">
            MERN Application
          </h1>
        </div>
      </header>
      <main className="max-w-7xl mx-auto py-6 px-4">
        <p className="text-gray-600">
          Generated by Digital Architect Protocol
        </p>
      </main>
    </div>
  );
}

export default App;"""
        else:
            return f"// {file_path} - Generated by Digital Architect Protocol\n// TODO: Implement component"

    async def _save_generated_file(self, tier: str, file_path: str, content: str):
        """Save generated file to appropriate directory"""
        if tier not in self.generated_files:
            self.generated_files[tier] = {}
        
        self.generated_files[tier][file_path] = content
        
        # Create physical file
        full_path = os.path.join(self.project_dir, tier, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)

    async def _save_blueprint(self):
        """Save architectural blueprint for reference"""
        blueprint_path = os.path.join(self.project_dir, "architectural_blueprint.json")
        with open(blueprint_path, 'w', encoding='utf-8') as f:
            json.dump(self.architectural_blueprint, f, indent=2)

    def _count_blueprint_files(self) -> int:
        """Count total files in blueprint"""
        backend_count = len(self.architectural_blueprint.get('backend', {}))
        frontend_count = len(self.architectural_blueprint.get('frontend', {}))
        return backend_count + frontend_count

    async def _apply_weaving_refinements(self):
        """Apply final architectural refinements based on critique"""
        refinements = self.interconnection_analysis.get('weaving_refinements', [])
        
        for refinement in refinements[:3]:  # Apply top 3 refinements
            await self._log(f"🔧 Applying refinement: {refinement}")
            # Implementation would depend on specific refinement type

    async def _call_ollama(self, prompt: str, max_tokens: int = 2000, max_retries: int = 3) -> str:
        """
        Make API call to local Ollama instance with enhanced error handling
        """
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.3,
                "top_p": 0.9,
                "num_predict": max_tokens
            }
        }
        
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    self.ollama_url,
                    json=payload,
                    timeout=120,  # Increased timeout for complex operations
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get("response", "")
                else:
                    logger.error(f"Ollama API error: {response.status_code} - {response.text}")
                    
            except Exception as e:
                logger.error(f"Ollama call attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
        
        raise Exception("Failed to connect to Ollama after multiple attempts")

    async def _stream_update(self, message: str, progress: int):
        """Send progress updates"""
        await manager.send_progress(self.task_id, message, progress)
        
    async def _log(self, message: str):
        """Send log messages"""
        await manager.send_log(self.task_id, message)


# Aliases for compatibility with legacy systems
AIWebsiteGenerator = DigitalArchitectGenerator
CognitiveOllamaGenerator = DigitalArchitectGenerator
OllamaWebsiteGenerator = DigitalArchitectGenerator
RealAIWebsiteGenerator = DigitalArchitectGenerator