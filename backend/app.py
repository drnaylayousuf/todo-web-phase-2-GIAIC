import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers import auth, tasks
from src.config import settings
from src.middleware.performance import PerformanceMiddleware
from src.database import create_db_and_tables
import uvicorn

# For Hugging Face Spaces, we need to make sure the database URL is properly configured
# Using SQLite for demo purposes or a PostgreSQL service
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./task_app.db")

# Override the database URL if we're on Hugging Face
if "hf.space" in os.getenv("HOSTNAME", ""):
    # For Hugging Face, you might need to use a cloud database
    # For demo purposes, we'll use SQLite
    DATABASE_URL = "sqlite:///./task_app_hf.db"

# Update settings to use the correct database URL
os.environ["DATABASE_URL"] = DATABASE_URL

def create_app():
    """Create and configure the FastAPI application"""
    app = FastAPI(
        title=settings.app_name,
        description="Full-stack web application for managing personal tasks with user authentication",
        version="1.0.0",
        debug=settings.debug,
    )

    # Add performance monitoring middleware
    app.add_middleware(PerformanceMiddleware)

    # Add CORS middleware - important for web interfaces
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # For Hugging Face Spaces
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Create database tables on startup
    @app.on_event("startup")
    def on_startup():
        create_db_and_tables()

    # Include routers
    app.include_router(auth.router, prefix="/api")  # Changed from settings.api_prefix to "/api" to match frontend expectations
    app.include_router(tasks.router, prefix="/api")

    @app.get("/")
    def read_root():
        return {"message": "Task CRUD API is running on Hugging Face Spaces!"}

    @app.get("/health")
    def health_check():
        return {"status": "healthy", "service": "task-crud-api", "platform": "huggingface-spaces"}

    return app

# Create the FastAPI app instance
app = create_app()

# For local testing
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))