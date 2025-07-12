import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # AI Provider Configuration
    AI_PROVIDER: str = "ollama"  # Options: "ollama" or "openai"
    OPENAI_API_KEY: Optional[str] = None
    
    # Ollama Configuration
    OLLAMA_API_URL: str = "http://localhost:11434/api/generate"
    OLLAMA_MAIN_MODEL: str = "mistral:latest"
    OLLAMA_CODE_MODEL: str = "deepseek-coder:6.7b"
    
    # File Storage
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    GENERATED_SITES_DIR: str = os.path.join(BASE_DIR, "generated_sites")
    MAX_CONCURRENT_JOBS: int = 5
    
    # WebSocket Configuration
    WS_HEARTBEAT_INTERVAL: int = 30
    
    # Task Configuration
    TASK_TIMEOUT_SECONDS: int = 600  # 10 minutes for large generations
    CLEANUP_INTERVAL_HOURS: int = 24
    
    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    
    # CORS Configuration
    CORS_ORIGINS: str = '["http://localhost:3000", "http://localhost:5173"]'
    
    # AI Model Configuration
    AI_MODEL: str = "gpt-4" if AI_PROVIDER == "openai" else "mistral:latest"
    AI_TEMPERATURE: float = 0.2
    AI_MAX_TOKENS: int = 4096
    AI_STREAMING: bool = True
    
    # MERN Generation Settings
    MERN_TEMPLATES_DIR: str = os.path.join(BASE_DIR, "app", "templates", "mern")
    DEFAULT_MERN_VERSION: str = "18.0.0"
    ENABLE_TYPESCRIPT: bool = True
    USE_YARN: bool = True
    
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