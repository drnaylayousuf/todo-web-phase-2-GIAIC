from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from uuid import UUID


class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=200, nullable=False)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)


class Task(TaskBase, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str = Field(min_length=1, max_length=200, nullable=False)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: UUID = Field(foreign_key="user.id", nullable=False, index=True)

    # Relationship with user
    owner: Optional["User"] = Relationship(back_populates="tasks")

# Removed custom __setattr__ method to avoid conflicts with SQLAlchemy initialization
# The updated_at field will be handled by SQLAlchemy events or manually when needed
from sqlalchemy import event


@event.listens_for(Task, 'before_update')
def update_updated_at(mapper, connection, target):
    from datetime import datetime as dt
    target.updated_at = dt.utcnow()


class TaskCreate(TaskBase):
    title: str
    description: Optional[str] = None


class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskRead(TaskBase):
    id: int
    user_id: UUID
    created_at: datetime
    updated_at: datetime