# Task CRUD Application with Authentication

A full-stack web application for managing personal tasks with user authentication, supporting create, read, update, delete operations with user data isolation.

## Features

- User registration and authentication
- Create, read, update, and delete tasks
- Task completion toggling
- User data isolation (users can only access their own tasks)
- Responsive web interface

## Tech Stack

- **Frontend**: Next.js 16+ with App Router, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python 3.12+
- **Database**: PostgreSQL with SQLModel ORM
- **Authentication**: JWT tokens with bcrypt password hashing
- **Styling**: Tailwind CSS with a consistent color scheme

## Architecture

The application follows a clean architecture with separation of concerns:

- `backend/`: FastAPI backend with models, schemas, services, and routers
- `frontend/`: Next.js frontend with pages, components, and API client

## Getting Started

### Prerequisites

- Python 3.12+
- Node.js 18+ (for frontend)
- PostgreSQL (or Docker for local development)

### Backend Setup

1. Install Python dependencies:
```bash
pip install -e .
```

2. Set up environment variables:
```bash
cp backend/.env.example backend/.env
# Edit backend/.env with your database URL and secret key
```

3. Run the application:
```bash
cd backend/src
python main.py
```

### Frontend Setup

1. Install Node.js dependencies:
```bash
cd frontend
npm install
```

2. Run the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000` and the backend at `http://localhost:8000`.

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and get JWT token

### Tasks
- `GET /api/tasks/` - Get all tasks for the authenticated user
- `POST /api/tasks/` - Create a new task
- `GET /api/tasks/{id}` - Get a specific task
- `PUT /api/tasks/{id}` - Update a task
- `PATCH /api/tasks/{id}/toggle` - Toggle task completion status
- `DELETE /api/tasks/{id}` - Delete a task

## Security

- Passwords are hashed using bcrypt
- JWT tokens for authentication with 7-day expiration
- User data isolation - users can only access their own tasks
- Input validation on both frontend and backend
- SQL injection prevention through parameterized queries

## Environment Variables

### Backend (.env)
- `DATABASE_URL` - PostgreSQL database connection string
- `SECRET_KEY` - Secret key for JWT token signing
- `ALGORITHM` - JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration time (default: 10080 minutes = 7 days)

### Frontend (.env.local)
- `NEXT_PUBLIC_API_BASE_URL` - Backend API base URL (default: http://localhost:8000/api)

## Development

The project follows a test-driven development approach with comprehensive documentation and clear separation of concerns. Each user story is implemented as an independent feature that can be tested separately.

## Deployment

This application can be deployed with the frontend on Vercel and the backend on Hugging Face Spaces. See the [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) file for detailed instructions on how to deploy both components.

### Quick Deployment Overview:

1. **Backend on Hugging Face Spaces**:
   - Deploy the `backend/` directory to a Hugging Face Space
   - Configure environment variables (DATABASE_URL, SECRET_KEY, etc.)
   - Note the Space URL for the next step

2. **Frontend on Vercel**:
   - Deploy the `frontend/` directory to Vercel
   - Set the `NEXT_PUBLIC_API_BASE_URL` environment variable to your Hugging Face Space backend URL
   - Your application will be live!

## Troubleshooting

### "Failed to fetch" Error

This error typically occurs when:
1. The backend server is not running
2. The backend server is running on a different port than expected
3. Network connectivity issues

To fix:
1. Verify the backend server is running with: `python run_backend.py`
2. Check that the `NEXT_PUBLIC_API_BASE_URL` in `.env` matches your backend address (should be `http://localhost:8000/api`)
3. Make sure both servers are accessible

### Running Both Servers

For development, you'll need two terminals:

Terminal 1 (Backend):
```bash
python run_backend.py
```

Terminal 2 (Frontend):
```bash
cd frontend && npm run dev
```

The backend will start on `http://localhost:8000` and the frontend on `http://localhost:3000`.

## License

[Add your license here]