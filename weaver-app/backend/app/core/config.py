import os
from pydantic_settings import BaseSettings
from typing import Optional, List

class Settings(BaseSettings):
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # OpenAI Configuration
    OPENAI_API_KEY: Optional[str] = None
    
    # File Storage
    GENERATED_SITES_DIR: str = "generated_sites"
    MAX_CONCURRENT_JOBS: int = 5
    
    # WebSocket Configuration
    WS_HEARTBEAT_INTERVAL: int = 30
    
    # Task Configuration
    TASK_TIMEOUT_SECONDS: int = 300  # 5 minutes
    CLEANUP_INTERVAL_HOURS: int = 24
    
    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    
    # CORS Configuration
    CORS_ORIGINS: str = '["http://localhost:3000", "http://localhost:5173"]'
    
    # AI Model Configuration
    AI_MODEL: str = "gpt-4"
    AI_TEMPERATURE: float = 0.3
    AI_MAX_TOKENS: int = 4000
    AI_STREAMING: bool = True
    
    # Quality Validation Settings
    QUALITY_THRESHOLD: int = 75
    ENABLE_GOLDEN_PROMPT_VALIDATION: bool = True
    
    # Security
    SECRET_KEY: str = "kodogen-ai-powered-website-generator-2025"
    
    class Config:
        env_file = ".env"
        extra = "ignore"  # Allow extra fields without validation errors

settings = Settings()