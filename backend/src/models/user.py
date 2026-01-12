from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid
from pydantic import validator


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True, nullable=False)


class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship with tasks
    tasks: List["Task"] = Relationship(back_populates="owner", cascade_delete=True)


# Define an event listener to update the updated_at field before update
from sqlalchemy import event
from datetime import datetime as dt

@event.listens_for(User, 'before_update')
def update_updated_at(mapper, connection, target):
    target.updated_at = dt.utcnow()



class UserCreate(UserBase):
    email: str
    password: str

    @validator('email')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Email must be valid')
        return v

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v


class UserRead(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime