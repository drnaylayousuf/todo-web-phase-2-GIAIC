from pydantic_settings import BaseSettings
from typing import Optional
import os
from urllib.parse import quote_plus
from pathlib import Path
from pydantic import field_validator, Field

# Load environment variables from .env file in the project root
from dotenv import load_dotenv
# Get the project root (two levels up from src directory)
project_root = Path(__file__).parent.parent.parent
dotenv_path = project_root / ".env"
load_dotenv(dotenv_path=dotenv_path)


class Settings(BaseSettings):
    model_config = {"env_file": str(project_root / ".env"), "extra": "ignore"}

    # Database settings
    database_url: str = Field(default="postgresql://user:password@localhost:5432/task_app", env="DATABASE_URL")
    db_echo: bool = Field(default=False, env="DB_ECHO")
    db_pool_size: int = Field(default=5, env="DB_POOL_SIZE")
    db_max_overflow: int = Field(default=10, env="DB_MAX_OVERFLOW")

    # JWT settings
    secret_key: str = Field(default="your-secret-key-change-in-production", env="SECRET_KEY")
    algorithm: str = Field(default="HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(default=10080, env="ACCESS_TOKEN_EXPIRE_MINUTES")  # 7 days

    # Application settings
    app_name: str = "Task CRUD API"
    debug: bool = Field(default=False, env="DEBUG")
    api_prefix: str = "/api/v1"

    @field_validator('db_echo', 'debug', mode='before')
    @classmethod
    def validate_bool(cls, v):
        if isinstance(v, bool):
            return v
        if isinstance(v, str):
            return v.strip().lower() in ('true', '1', 'yes', 'on')
        return bool(v)


settings = Settings()