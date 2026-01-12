# Development Quickstart Guide: Task CRUD Operations with Authentication

**Date**: 2026-01-01
**Feature**: Task CRUD Operations with Authentication
**Branch**: 001-task-crud-auth

## Prerequisites

- Docker 20.10+
- Docker Compose v2+
- Git
- Node.js 18+ (for local development without Docker)
- Python 3.13+ (for local development without Docker)

## Quick 3-Step Setup

### 1. Clone and Setup Environment
```bash
# Clone the repository
git clone <your-repo-url>
cd <your-repo-name>

# Copy environment files
cp frontend/.env.example frontend/.env.local
cp backend/.env.example backend/.env

# Update environment variables as needed
```

### 2. Configure Environment Variables
In `backend/.env`:
- `DATABASE_URL=postgresql://user:password@localhost:5432/taskdb`
- `JWT_SECRET=your-super-secret-jwt-key-here`
- `BCRYPT_ROUNDS=12`

In `frontend/.env.local`:
- `NEXT_PUBLIC_API_URL=http://localhost:8000`

### 3. Start Development Environment
```bash
# Start all services with Docker Compose
docker-compose up --build

# Or to run in detached mode
docker-compose up --build -d
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Database: localhost:5432 (PostgreSQL)

## Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend       │    │   Database      │
│  (Next.js)      │◄──►│   (FastAPI)      │◄──►│ (PostgreSQL)    │
│  Port 3000      │    │   Port 8000      │    │   Port 5432     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Development Workflow

### Hot Reload
- Frontend: Changes to React components automatically reload
- Backend: Changes to Python files automatically reload
- Both services are configured for fast development iteration

### Testing
```bash
# Run backend tests
docker-compose exec backend pytest

# Run frontend tests
docker-compose exec frontend npm test

# Run end-to-end tests
docker-compose exec frontend npx playwright test
```

### Database Migrations
```bash
# Run migrations
docker-compose exec backend alembic upgrade head

# Create new migration
docker-compose exec backend alembic revision --autogenerate -m "migration message"

# Check migration status
docker-compose exec backend alembic current
```

## API Documentation
- Backend API: http://localhost:8000/docs (Swagger UI)
- Backend Redoc: http://localhost:8000/redoc (Redoc UI)

## Troubleshooting

### Common Issues

**Port Conflicts**: If ports 3000, 8000, or 5432 are in use:
- Update ports in `docker-compose.yml`
- Update corresponding environment variables

**Database Connection Issues**:
- Verify database service is running: `docker-compose ps`
- Check database logs: `docker-compose logs database`
- Ensure environment variables match in backend service

**Authentication Issues**:
- Verify JWT_SECRET is consistent between services
- Check that httpOnly cookies are enabled in browser
- Confirm CORS settings in backend

**Migration Issues**:
- Run migrations after database starts: `docker-compose exec backend alembic upgrade head`
- Check database connection string in environment

### Useful Commands
```bash
# View all service logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend

# Run backend commands
docker-compose exec backend bash

# Run frontend commands
docker-compose exec frontend bash

# Stop all services
docker-compose down

# Stop and remove volumes (removes data)
docker-compose down -v
```

## Production Deployment Checklist

### Before Production
- [ ] Update JWT secret to secure value
- [ ] Configure production database (Neon Serverless)
- [ ] Set up proper logging and monitoring
- [ ] Configure SSL/TLS certificates
- [ ] Set up health checks
- [ ] Configure resource limits

### Environment Variables
- [ ] `DATABASE_URL` points to production database
- [ ] `JWT_SECRET` is a secure, long random string
- [ ] `NODE_ENV` and `ENVIRONMENT` set to 'production'
- [ ] Logging level set appropriately

## Performance Optimization Tips

### Database
- Ensure proper indexing (user_id, completed status)
- Monitor slow queries with PostgreSQL logging
- Consider connection pooling settings

### Frontend
- Enable gzip compression
- Optimize image loading
- Implement proper caching strategies
- Use production build for deployment

### Backend
- Monitor API response times
- Optimize database queries
- Consider async operations for I/O bound tasks
- Implement proper error handling and logging

## Security Notes

### Data Isolation
- ALL database queries must filter by user_id
- Return 404 (not 403) for unauthorized access attempts
- JWT validation required for all protected endpoints
- Passwords must be hashed with bcrypt

### Authentication
- JWT tokens stored in httpOnly cookies
- 7-day token expiration
- Secure cookie attributes (SameSite, Secure)
- Rate limiting for authentication endpoints (future enhancement)