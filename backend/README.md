# Task Manager Backend

This is the backend for the Task Manager application, built with FastAPI and SQLModel.

## Deployment on Hugging Face Spaces

This application can be deployed on Hugging Face Spaces as a Docker container or using the Gradio runner.

### Environment Variables

- `DATABASE_URL`: PostgreSQL database connection string (e.g., `postgresql://user:password@host:port/dbname`) or use SQLite for simpler setups
- `SECRET_KEY`: Secret key for JWT token signing (generate a strong random key)
- `ALGORITHM`: JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time (default: 10080 minutes = 7 days)

### Deployment Steps

#### Option 1: Using the Space Runner (Recommended for Gradio apps)

1. Fork this repository
2. Go to [Hugging Face Spaces](https://huggingface.co/spaces) and create a new Space
3. Choose "Docker" or "CPU" space type
4. Connect to your forked repository
5. Make sure your `app.py` contains the FastAPI app instance as `app`
6. Add the required environment variables in the Space settings

#### Option 2: Direct Docker Deployment

If deploying via Docker, ensure you have:
- `app.py` with the FastAPI app instance as `app`
- `requirements.txt` with all dependencies
- Proper environment variables configured

### Local Testing

```bash
pip install -r requirements.txt
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Important Notes

- For Hugging Face Spaces, the application will be served at the root path
- The API endpoints will be available at `/api/auth` and `/api/tasks`
- For persistent storage on Hugging Face Spaces, consider using an external PostgreSQL database as files may not persist between restarts
- The application expects the database to be available at the URL specified in DATABASE_URL

## API Endpoints

- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/tasks/` - Get all tasks for the authenticated user
- `POST /api/tasks/` - Create a new task
- `GET /api/tasks/{id}` - Get a specific task
- `PUT /api/tasks/{id}` - Update a task
- `PATCH /api/tasks/{id}/toggle` - Toggle task completion status
- `DELETE /api/tasks/{id}` - Delete a task