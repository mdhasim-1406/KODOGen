import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # OpenAI Configuration
    OPENAI_API_KEY: Optional[str] = None
    
    # File Storage
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    GENERATED_SITES_DIR: str = os.path.join(BASE_DIR, "generated_sites")
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
    AI_MODEL: str = "mistral:latest"
    AI_TEMPERATURE: float = 0.2
    AI_MAX_TOKENS: int = 4096
    AI_STREAMING: bool = True
    
    # Quality Validation Settings
    QUALITY_THRESHOLD: int = 80
    ENABLE_GOLDEN_PROMPT_VALIDATION: bool = True
    
    # Security
    SECRET_KEY: str = "kodogen-ai-powered-website-generator-2025"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        extra='ignore'
    )

settings = Settings()