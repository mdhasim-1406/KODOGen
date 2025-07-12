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
        
        # Olloma configuration with multiple models
        self.olloma_url = "http://localhost:11434/api/generate"
        self.main_model = "mistral:latest"  # For architecture and analysis
        self.code_model = "deepseek-coder:1.3b"  # For code generation
        
        # Digital Architect state
        self.architectural_blueprint = None
        self.generated_files = {}
        self.dependency_graph = {}
        self.weaving_quality_score = 0
        self.interconnection_analysis = {}
        
    async def generate_mern_application(self) -> None:
        """
        Main orchestrator for Digital Architect Protocol with Protocol Vesta instrumentation
        """
        try:
            await self._log("✅ [START] Weaver Protocol initiated...")
            await self._stream_update("🏗️ Dr. Reed initializing Digital Architect Protocol...", 5)
            
            # Create project directory structure
            os.makedirs(self.project_dir, exist_ok=True)
            await self._log(f"📁 [INIT] Created project directory: {self.project_dir}")
            
            # ARCHITECT PHASE 1: Application Blueprinting
            await self._stream_update("🧠 Digital Architect designing system blueprint...", 10)
            await self._log("⚙️ [PLAN] Generating architectural blueprint...")
            self.architectural_blueprint = await self._generate_architectural_blueprint()
            
            if not self.architectural_blueprint:
                await self._log("❌ [PLAN] Failed to generate architectural blueprint")
                raise Exception("Failed to generate architectural blueprint")
            
            file_count = self._count_blueprint_files()
            await self._log(f"✅ [PLAN] Blueprint received with {file_count} files planned")
            
            # Save blueprint for reference
            await self._save_blueprint()
            await self._log("📝 [SAVE] Architectural blueprint saved to disk")
            
            # ARCHITECT PHASE 2: Hierarchical Generation
            await self._log("🔄 [LOOP] Starting backend generation...")
            await self._stream_update("🔧 Weaving backend infrastructure...", 20)
            await self._generate_backend_tier()
            
            # Validate backend generation
            backend_files = len(self.generated_files.get('backend', {}))
            await self._log(f"✅ [TIER] Backend tier complete: {backend_files} files")
            
            await self._log("🔄 [LOOP] Starting frontend generation...")
            await self._stream_update("⚛️ Weaving frontend ecosystem...", 60)
            await self._generate_frontend_tier()
            
            # Validate frontend generation
            frontend_files = len(self.generated_files.get('frontend', {}))
            await self._log(f"✅ [TIER] Frontend tier complete: {frontend_files} files")
            
            # Validation Phase
            total_files = backend_files + frontend_files
            if total_files == 0:
                await self._log("❌ [VALIDATE] No files were generated")
                raise Exception("No files were generated during the process")
            
            await self._log(f"✅ [VALIDATE] Generated {total_files} files successfully")
            
            # ARCHITECT PHASE 3: Full-Stack Self-Critique
            await self._stream_update("🔍 Dr. Reed analyzing system interconnectivity...", 85)
            await self._log("⚙️ [CRITIQUE] Performing system analysis...")
            await self._perform_fullstack_critique()
            
            # ARCHITECT PHASE 4: Final Weaving Refinements
            await self._stream_update("✨ Applying architectural refinements...", 95)
            await self._apply_weaving_refinements()
            
            await self._stream_update(f"🎉 Digital ecosystem complete! Generated {total_files} files", 100)
            await self._log(f"🏆 [COMPLETE] System Weaving Score: {self.weaving_quality_score}/10")
            
            # Send completion notification
            preview_url = f"/api/preview/{self.task_id}/"
            download_url = f"/api/download/{self.task_id}"
            await manager.send_completion(self.task_id, preview_url, download_url)
            
        except Exception as e:
            logger.error(f"Digital Architect Error: {e}")
            await self._log(f"❌ [ERROR] System weaving failed: {str(e)}")
            await manager.send_error(self.task_id, f"Generation failed: {str(e)}")
            raise

    async def _generate_architectural_blueprint(self) -> Dict:
        """
        ARCHITECT PHASE 1: Generate comprehensive system architecture
        """
        blueprint_prompt = self._get_application_blueprint_prompt()
        
        try:
            response = await self._call_ollama(blueprint_prompt, max_tokens=4096)
            
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
        """Generate backend in dependency order with enhanced validation"""
        await self._log("🔄 [PHASE] Starting backend tier generation")
        
        backend_files = self.architectural_blueprint.get('backend', {})
        if not backend_files:
            await self._log("⚠️ [WARN] No backend files defined in blueprint")
            return
            
        generation_order = [
            'package.json',
            'models/',
            'controllers/',
            'routes/',
            'middleware/',
            'server.js',
            '.env'
        ]
        
        files_generated = 0
        total_files = len(backend_files)
        
        for file_pattern in generation_order:
            matching_files = [f for f in backend_files.keys() if file_pattern in f]
            
            for file_path in matching_files:
                try:
                    await self._stream_update(f"🔧 WEAVING BACKEND > /{file_path}...", None)
                    await self._log(f"⚙️ [GEN] Generating backend file: {file_path}")
                    
                    file_content = await self._generate_backend_file(file_path, backend_files[file_path])
                    if not file_content or not file_content.strip():
                        await self._log(f"❌ [ERROR] Empty content generated for {file_path}")
                        continue
                        
                    await self._save_generated_file('backend', file_path, file_content)
                    files_generated += 1
                    await self._log(f"✅ [GEN] Backend file created ({files_generated}/{total_files}): {file_path}")
                    
                except Exception as e:
                    await self._log(f"❌ [ERROR] Failed to generate {file_path}: {str(e)}")
                    continue
        
        await self._log(f"📊 [PHASE] Backend generation complete: {files_generated}/{total_files} files created")

    async def _generate_frontend_tier(self):
        """Generate frontend in dependency order with enhanced validation"""
        await self._log("🔄 [PHASE] Starting frontend tier generation")
        
        frontend_files = self.architectural_blueprint.get('frontend', {})
        if not frontend_files:
            await self._log("⚠️ [WARN] No frontend files defined in blueprint")
            return
            
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
        
        files_generated = 0
        total_files = len(frontend_files)
        
        for file_pattern in generation_order:
            matching_files = [f for f in frontend_files.keys() if file_pattern in f]
            
            for file_path in matching_files:
                try:
                    await self._stream_update(f"⚛️ WEAVING FRONTEND > /{file_path}...", None)
                    await self._log(f"⚙️ [GEN] Generating frontend file: {file_path}")
                    
                    file_content = await self._generate_frontend_file(file_path, frontend_files[file_path])
                    if not file_content or not file_content.strip():
                        await self._log(f"❌ [ERROR] Empty content generated for {file_path}")
                        continue
                        
                    await self._save_generated_file('frontend', file_path, file_content)
                    files_generated += 1
                    await self._log(f"✅ [GEN] Frontend file created ({files_generated}/{total_files}): {file_path}")
                    
                except Exception as e:
                    await self._log(f"❌ [ERROR] Failed to generate {file_path}: {str(e)}")
                    continue
        
        await self._log(f"📊 [PHASE] Frontend generation complete: {files_generated}/{total_files} files created")

    async def _generate_backend_file(self, file_path: str, description: str) -> str:
        """Generate individual backend file with system context using code-specialized model"""
        await self._log(f"🔄 [LOOP] Generating backend file: {file_path}")
        
        # First, check if we have valid blueprint
        if not self.architectural_blueprint:
            await self._log(f"❌ [ERROR] Cannot generate {file_path}: No architectural blueprint")
            return self._get_fallback_backend_file(file_path)
            
        backend_prompt = f"""You are Dr. Evelyn Reed, generating a backend file for a MERN application.

APPLICATION CONTEXT:
- User Request: {self.prompt}
- Project: {self.architectural_blueprint.get('project_name', 'mern-app')}
- File: {file_path}
- Purpose: {description}

ARCHITECTURAL BLUEPRINT CONTEXT:
{json.dumps(self.architectural_blueprint, indent=2)}

Instructions for {file_path}:
- Generate complete, working code for this specific file
- Follow MERN best practices and patterns
- Include proper error handling
- Use modern ES6+ JavaScript
- Add JSDoc documentation
- Include proper data validation
- Handle edge cases appropriately

Focus on this file's role:
{self._get_file_specific_instructions(file_path)}

Generate ONLY the file content, no explanations or markdown:"""

        try:
            await self._log(f"⚙️ [AI-CODE] Requesting code for {file_path}...")
            # Use code model by default for file generation
            response = await self._call_ollama(backend_prompt, max_tokens=3000, use_code_model=True)
            
            if not response or not response.strip():
                await self._log(f"❌ [AI-CODE] Empty response for {file_path}")
                return self._get_fallback_backend_file(file_path)
            
            # Validate the generated content
            cleaned_content = self._clean_generated_code(response.strip())
            if not self._validate_generated_code(cleaned_content, file_path):
                await self._log(f"❌ [AI-CODE] Invalid code generated for {file_path}")
                return self._get_fallback_backend_file(file_path)
                
            await self._log(f"✅ [AI-CODE] Code received and validated for {file_path}")
            return cleaned_content
            
        except Exception as e:
            logger.error(f"Backend file generation failed for {file_path}: {e}")
            await self._log(f"❌ [AI-CODE] Failed to generate {file_path}: {str(e)}")
            return self._get_fallback_backend_file(file_path)
            
    def _get_file_specific_instructions(self, file_path: str) -> str:
        """Get specific instructions based on file type"""
        if 'controllers' in file_path:
            return """This is a controller file:
- Implement all CRUD operations
- Include proper error handling for each route
- Add input validation
- Use try-catch blocks for database operations
- Return appropriate HTTP status codes
- Add proper success/error responses"""
        elif 'models' in file_path:
            return """This is a Mongoose model:
- Define the schema with proper types
- Add field validations
- Include timestamps
- Add proper indexes
- Define instance methods if needed
- Add static methods if needed"""
        elif 'routes' in file_path:
            return """This is a route file:
- Define all REST endpoints
- Add proper middleware
- Include input validation
- Use correct HTTP methods
- Link to appropriate controller methods"""
        elif 'server.js' in file_path:
            return """This is the main server file:
- Configure Express server
- Set up middleware
- Connect to MongoDB
- Import and use routes
- Handle errors
- Set up CORS"""
        else:
            return "Generate complete, working code for this file following best practices."
            
    def _clean_generated_code(self, content: str) -> str:
        """Clean up generated code"""
        # Remove markdown code blocks if present
        content = content.replace('```javascript', '').replace('```', '')
        # Remove leading/trailing whitespace
        content = content.strip()
        # Ensure proper EOF newline
        if not content.endswith('\n'):
            content += '\n'
        return content
        
    def _validate_generated_code(self, content: str, file_path: str) -> bool:
        """Validate generated code for common issues"""
        # Check for minimum content length
        if len(content) < 50:  # Arbitrary minimum for a meaningful file
            return False
            
        # Check for basic syntax issues
        try:
            # Basic syntax validation
            if not content.strip():
                return False
                
            # Check for TODO comments
            if 'TODO: Implement' in content:
                return False
                
            # File-specific validations
            if 'controllers' in file_path:
                required_patterns = ['exports', 'async', 'try', 'catch']
                return all(pattern in content for pattern in required_patterns)
                
            if 'models' in file_path:
                required_patterns = ['mongoose', 'Schema', 'module.exports']
                return all(pattern in content for pattern in required_patterns)
                
            if 'routes' in file_path:
                required_patterns = ['router', 'express', 'module.exports']
                return all(pattern in content for pattern in required_patterns)
                
            return True
            
        except Exception:
            return False

    async def _generate_frontend_file(self, file_path: str, description: str) -> str:
        """Generate individual frontend file with system context using code-specialized model"""
        await self._log(f"🔄 [LOOP] Generating frontend file: {file_path}")
        
        frontend_prompt = f"""You are Dr. Evelyn Reed, generating a frontend file for a MERN application.

APPLICATION CONTEXT:
- User Request: {self.prompt}
- Project: {self.architectural_blueprint.get('project_name', 'mern-app')}
- File: {file_path}
- Purpose: {description}

ARCHITECTURAL BLUEPRINT CONTEXT:
{json.dumps(self.architectural_blueprint, indent=2)}

Instructions for {file_path}:
- Generate complete, working code for this specific file
- Use modern React patterns (hooks, functional components)
- Implement proper state management with Zustand
- Include TypeScript types where applicable
- Follow React best practices
- Add proper error boundaries
- Include loading states
- Use proper commenting and documentation

Focus on this file's role:
{self._get_frontend_file_instructions(file_path)}

Generate ONLY the file content, no explanations or markdown:"""

        try:
            await self._log(f"⚙️ [AI-CODE] Requesting code for {file_path}...")
            response = await self._call_ollama(frontend_prompt, max_tokens=3000, use_code_model=True)
            
            if not response or not response.strip():
                await self._log(f"❌ [AI-CODE] Empty response for {file_path}")
                return self._get_fallback_frontend_file(file_path)
                
            # Clean and validate the code
            cleaned_content = self._clean_generated_code(response.strip())
            if not self._validate_frontend_code(cleaned_content, file_path):
                await self._log(f"❌ [AI-CODE] Invalid code generated for {file_path}")
                return self._get_fallback_frontend_file(file_path)
                
            await self._log(f"✅ [AI-CODE] Code received and validated for {file_path}")
            return cleaned_content
            
        except Exception as e:
            logger.error(f"Frontend file generation failed for {file_path}: {e}")
            await self._log(f"⚠️ Using fallback for {file_path} due to: {str(e)}")
            return self._get_fallback_frontend_file(file_path)
            
    def _get_frontend_file_instructions(self, file_path: str) -> str:
        """Get specific instructions based on frontend file type"""
        if 'components' in file_path:
            return """This is a React component:
- Use functional components
- Implement proper prop types
- Add error boundaries
- Include loading states
- Use proper event handling
- Implement proper styling"""
        elif 'store' in file_path:
            return """This is a Zustand store:
- Define proper state structure
- Implement state updates
- Add proper typing
- Include API integration
- Handle loading and error states"""
        elif 'api' in file_path:
            return """This is an API service:
- Use Axios for requests
- Include error handling
- Add request/response interceptors
- Implement proper typing
- Add retry logic"""
        elif 'App.jsx' in file_path:
            return """This is the main App component:
- Set up routing
- Include layout components
- Add error boundaries
- Set up global providers
- Handle authentication state"""
        else:
            return "Generate complete, working React code following best practices."
            
    def _validate_frontend_code(self, content: str, file_path: str) -> bool:
        """Validate generated frontend code"""
        if len(content) < 50:
            return False
            
        try:
            if not content.strip():
                return False
                
            if 'TODO: Implement' in content:
                return False
                
            # File-specific validations
            if 'components' in file_path:
                required_patterns = ['import React', 'export default', 'function']
                return all(pattern in content for pattern in required_patterns)
                
            if 'store' in file_path:
                required_patterns = ['create', 'state', 'export']
                return all(pattern in content for pattern in required_patterns)
                
            if 'api' in file_path:
                required_patterns = ['axios', 'export', 'async']
                return all(pattern in content for pattern in required_patterns)
                
            return True
            
        except Exception:
            return False

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
        """Save generated file to appropriate directory with enhanced validation"""
        try:
            if not content or not content.strip():
                await self._log(f"⚠️ [SAVE] Empty content for {file_path}, skipping file creation")
                return

            if tier not in self.generated_files:
                self.generated_files[tier] = {}
            
            self.generated_files[tier][file_path] = content
            
            # Create physical file with full path validation
            full_path = os.path.join(self.project_dir, tier, file_path)
            await self._log(f"📝 [SAVE] Creating file at: {full_path}")
            
            # Ensure the directory exists
            dir_path = os.path.dirname(full_path)
            if not os.path.exists(dir_path):
                await self._log(f"📁 [SAVE] Creating directory: {dir_path}")
                os.makedirs(dir_path, exist_ok=True)
            
            # Write file with content validation
            with open(full_path, 'w', encoding='utf-8') as f:
                bytes_written = f.write(content)
                await self._log(f"✅ [SAVE] Wrote {bytes_written} bytes to {file_path}")
            
            # Verify file was created and has content
            if not os.path.exists(full_path):
                raise Exception(f"File {file_path} was not created")
                
            if os.path.getsize(full_path) == 0:
                raise Exception(f"File {file_path} was created but is empty")
            
            await self._log(f"✅ [SAVE] File saved and verified: {file_path}")
            
        except Exception as e:
            error_msg = f"Failed to save file {file_path}: {str(e)}"
            logger.error(error_msg)
            await self._log(f"❌ [SAVE] {error_msg}")
            raise  # Re-raise to handle in the main generation flow

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

    async def _call_ollama(self, prompt: str, max_tokens: int = 4096, max_retries: int = 3, use_code_model: bool = False) -> str:
        """
        Make API call to local Ollama instance with enhanced error handling and smart model selection.
        
        Args:
            prompt (str): The prompt to send to the model
            max_tokens (int): Maximum number of tokens to generate
            max_retries (int): Number of retry attempts on failure
            use_code_model (bool): Force using code-specialized model
            
        Returns:
            str: Generated response text
            
        Raises:
            Exception: If all retry attempts fail or model is not available
        """
        import aiohttp
        import async_timeout

        # Smart model selection based on task complexity and content
        model = self.code_model if (use_code_model or 'Generate ONLY the file content' in prompt) else self.main_model
        
        # Optimize parameters based on task type
        temperature = 0.2 if use_code_model else 0.4  # Lower temp for code generation
        top_p = 0.95 if use_code_model else 0.9
        top_k = 40 if use_code_model else 20
        
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "top_p": top_p,
                "top_k": top_k,
                "num_predict": max_tokens,
                "stop": ["```"] if use_code_model else None
            }
        }
        
        # Enhanced error handling with detailed logging
        last_error = None
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                    await self._log(f"🔄 Retrying Ollama call (attempt {attempt + 1}/{max_retries}) with model {model}")
                
                async with aiohttp.ClientSession() as session:
                    async with async_timeout.timeout(150):  # 2.5 minute timeout
                        async with session.post(self.olloma_url, json=payload) as response:
                            if response.status == 200:
                                result = await response.json()
                                return result.get("response", "")
                            elif response.status == 404:
                                error_text = await response.text()
                                if "model not found" in error_text.lower():
                                    # Try falling back to main model if code model fails
                                    if model == self.code_model and self.main_model != model:
                                        await self._log(f"⚠️ Code model not found, falling back to {self.main_model}")
                                        model = self.main_model
                                        payload["model"] = model
                                        continue
                                    error_msg = f"Model {model} not found. Please ensure it's installed with 'olloma pull {model}'"
                                    await self._log(f"❌ {error_msg}", "error")
                                    raise Exception(error_msg)
                            
                            last_error = f"Ollama API error: {response.status} - {await response.text()}"
                            logger.error(last_error)
                    
            except asyncio.TimeoutError:
                last_error = f"Ollama API timeout on attempt {attempt + 1}"
                logger.error(last_error)
                await self._log(f"⚠️ {last_error}")
            except Exception as e:
                last_error = str(e)
                logger.error(f"Ollama call error on attempt {attempt + 1}: {e}")
                await self._log(f"⚠️ Error: {last_error}")
        
        # All retries failed
        error_msg = f"Failed to connect to Ollama after {max_retries} attempts. Last error: {last_error}"
        await self._log(f"❌ {error_msg}")
        raise Exception(error_msg)

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