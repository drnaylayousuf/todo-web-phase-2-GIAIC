from pydantic_settings import BaseSettings
from typing import Optional
import os
from urllib.parse import quote_plus
from pathlib import Path

# Load environment variables from .env file in the project root
from dotenv import load_dotenv
# Get the project root (two levels up from src directory)
project_root = Path(__file__).parent.parent.parent
dotenv_path = project_root / ".env"
load_dotenv(dotenv_path=dotenv_path)


class Settings(BaseSettings):
    # Database settings
    database_url: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/task_app")
    db_echo: bool = os.getenv("DB_ECHO", "False").lower() == "true"
    db_pool_size: int = int(os.getenv("DB_POOL_SIZE", "5"))
    db_max_overflow: int = int(os.getenv("DB_MAX_OVERFLOW", "10"))

    # JWT settings
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "10080"))  # 7 days

    # Application settings
    app_name: str = "Task CRUD API"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    api_prefix: str = "/api/v1"


settings = Settings()