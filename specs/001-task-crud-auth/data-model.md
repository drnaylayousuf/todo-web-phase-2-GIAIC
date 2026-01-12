# Database Schema & Data Models: Task CRUD Operations with Authentication

**Date**: 2026-01-03
**Feature**: Task CRUD Operations with Authentication
**Branch**: 001-task-crud-auth

## Entity Relationship Model

### User Entity

**Attributes**:
- `id`: UUID (Primary Key, default: gen_random_uuid())
- `email`: VARCHAR(255), UNIQUE, NOT NULL
- `password_hash`: VARCHAR(255), NOT NULL
- `created_at`: TIMESTAMP WITH TIME ZONE, NOT NULL, default: current_timestamp
- `updated_at`: TIMESTAMP WITH TIME ZONE, NOT NULL, default: current_timestamp

**Indexes**:
- `idx_users_email`: ON (email) - UNIQUE INDEX for fast email lookups
- `idx_users_created_at`: ON (created_at) - for sorting and filtering

**Constraints**:
- `users_email_unique`: UNIQUE (email)
- `users_email_not_empty`: CHECK (email <> '')
- `users_email_format`: CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')

**Relationships**:
- One User → Many Tasks (ON DELETE CASCADE)

### Task Entity

**Attributes**:
- `id`: SERIAL (Primary Key)
- `user_id`: UUID, NOT NULL, FOREIGN KEY references users(id)
- `title`: VARCHAR(200), NOT NULL
- `description`: TEXT, NULL
- `completed`: BOOLEAN, NOT NULL, default: false
- `created_at`: TIMESTAMP WITH TIME ZONE, NOT NULL, default: current_timestamp
- `updated_at`: TIMESTAMP WITH TIME ZONE, NOT NULL, default: current_timestamp

**Indexes**:
- `idx_tasks_user_id`: ON (user_id) - for user-based filtering
- `idx_tasks_completed`: ON (completed) - for completion status filtering
- `idx_tasks_user_completed`: ON (user_id, completed) - composite index for common queries
- `idx_tasks_created_at`: ON (created_at) - for sorting and pagination

**Constraints**:
- `tasks_title_not_empty`: CHECK (title <> '')
- `tasks_title_length`: CHECK (length(title) >= 1 AND length(title) <= 200)
- `tasks_description_length`: CHECK (length(description) <= 1000)

**Relationships**:
- Many Tasks ← One User (user_id FK)

## SQL Schema Definition

```sql
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Create tasks table
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Create indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
CREATE INDEX idx_tasks_user_completed ON tasks(user_id, completed);
CREATE INDEX idx_tasks_created_at ON tasks(created_at);

-- Add check constraints
ALTER TABLE users
ADD CONSTRAINT users_email_not_empty
CHECK (email <> ''),
ADD CONSTRAINT users_email_format
CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$');

ALTER TABLE tasks
ADD CONSTRAINT tasks_title_not_empty
CHECK (title <> ''),
ADD CONSTRAINT tasks_title_length
CHECK (length(title) >= 1 AND length(title) <= 200),
ADD CONSTRAINT tasks_description_length
CHECK (length(description) <= 1000);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers to automatically update updated_at
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_tasks_updated_at
    BEFORE UPDATE ON tasks
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

## Database Security Patterns

### Critical Security Pattern: User Data Isolation
**All database queries must filter by WHERE user_id = current_user.id**

This pattern ensures that users can only access their own data:
- SELECT queries: `SELECT * FROM tasks WHERE user_id = $1`
- UPDATE queries: `UPDATE tasks SET ... WHERE id = $1 AND user_id = $2`
- DELETE queries: `DELETE FROM tasks WHERE id = $1 AND user_id = $2`

### Authentication Security
- Passwords must be hashed with bcrypt before database storage
- No plaintext passwords in the database
- Use parameterized queries to prevent SQL injection
- JWT validation happens at the application layer before DB access

## Migration Strategy

### Using Alembic for Database Migrations

**Initial Migration (001_initial_schema.py)**:
```python
# Initial schema migration
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    # Create UUID extension
    op.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\"")

    # Create users table
    op.create_table('users',
        sa.Column('id', postgresql.UUID(as_uuid=True),
                 server_default=sa.text('gen_random_uuid()'),
                 nullable=False),
        sa.Column('email', sa.VARCHAR(255), nullable=False),
        sa.Column('password_hash', sa.VARCHAR(255), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True),
                 server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True),
                 server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

    # Create tasks table
    op.create_table('tasks',
        sa.Column('id', sa.Integer, autoincrement=True, nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.VARCHAR(200), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('completed', sa.Boolean, server_default='false', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True),
                 server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True),
                 server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE')
    )

    # Create indexes
    op.create_index('idx_users_email', 'users', ['email'])
    op.create_index('idx_users_created_at', 'users', ['created_at'])

    op.create_index('idx_tasks_user_id', 'tasks', ['user_id'])
    op.create_index('idx_tasks_completed', 'tasks', ['completed'])
    op.create_index('idx_tasks_user_completed', 'tasks', ['user_id', 'completed'])
    op.create_index('idx_tasks_created_at', 'tasks', ['created_at'])

def downgrade():
    op.drop_index('idx_tasks_created_at', table_name='tasks')
    op.drop_index('idx_tasks_user_completed', table_name='tasks')
    op.drop_index('idx_tasks_completed', table_name='tasks')
    op.drop_index('idx_tasks_user_id', table_name='tasks')

    op.drop_index('idx_users_created_at', table_name='users')
    op.drop_index('idx_users_email', table_name='users')

    op.drop_table('tasks')
    op.drop_table('users')

    op.execute("DROP EXTENSION IF EXISTS \"uuid-ossp\"")
```

## SQLModel Implementation

### User Model (backend/src/models/user.py)
```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid

class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False, max_length=255)

class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    password_hash: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)

    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="user")

class UserRead(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

class UserCreate(UserBase):
    password: str  # Plain text password that will be hashed

class UserUpdate(SQLModel):
    email: Optional[str] = None
```

### Task Model (backend/src/models/task.py)
```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
import uuid

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)

class Task(TaskBase, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", nullable=False, ondelete="CASCADE")
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)

    # Relationship to user
    user: "User" = Relationship(back_populates="tasks")

class TaskRead(TaskBase):
    id: int
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

class TaskCreate(TaskBase):
    pass

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
```

## API Schema Models (Pydantic)

### User Schemas (backend/src/schemas/user.py)
```python
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import uuid

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

class UserUpdate(BaseModel):
    email: Optional[str] = None
```

### Task Schemas (backend/src/schemas/task.py)
```python
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import uuid

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TaskCreate(TaskBase):
    pass

class TaskRead(TaskBase):
    id: int
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
```

## Security Considerations

### Database-Level Security
- All queries must filter by user_id to ensure data isolation
- Use of parameterized queries to prevent SQL injection
- Proper indexing for performance and security
- UUID for user IDs to prevent enumeration attacks
- Automatic updated_at timestamp updates via triggers

### Application-Level Security
- JWT validation before any database access
- User ID extracted from JWT token and used for queries
- Return 404 (not 403) for unauthorized access attempts
- Input validation via Pydantic schemas
- Password hashing with bcrypt before storage

## Performance Considerations

### Indexing Strategy
- Index on user_id for user-based queries
- Index on completed for status filtering
- Composite index on (user_id, completed) for common queries
- Index on created_at for sorting and pagination

### Query Optimization
- Use EXPLAIN ANALYZE to verify query performance
- Avoid N+1 queries with proper relationship loading
- Use pagination for large datasets
- Consider read replicas for read-heavy operations