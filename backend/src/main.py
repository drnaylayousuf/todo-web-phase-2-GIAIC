from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, tasks
from .config import settings
from .middleware.performance import PerformanceMiddleware
from .database import create_db_and_tables


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

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, specify your frontend domain
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
        return {"message": "Task CRUD API is running!"}

    @app.get("/health")
    def health_check():
        return {"status": "healthy", "service": "task-crud-api"}

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )