# backend/app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "RTOS V2X Intelligent Operations Platform"
    API_V1_STR: str = "/api/v1"

    # Database settings (example, to be filled from .env)
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "aiops_db"
    # SQLALCHEMY_DATABASE_URI: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}"
    # The above line causes issues if POSTGRES_USER etc. are not defined at class creation time
    # A property or a validator would be better if we want to construct it from other settings.
    # For now, allow it to be set directly or from .env
    SQLALCHEMY_DATABASE_URI: str = "postgresql://postgres:password@localhost/aiops_db"


    # LLM settings (example)
    OLLAMA_API_BASE: str = "http://localhost:11434"

    class Config:
        case_sensitive = True
        env_file = ".env" # For local development, load from .env
        env_file_encoding = 'utf-8'

settings = Settings()
