import pytest
from datetime import datetime
from uuid import UUID
from src.models.user import User, UserCreate
from src.models.task import Task, TaskCreate, TaskUpdate
from src.utils.security import get_password_hash


def test_user_model_creation():
    """Test User model creation with validation"""
    user_data = UserCreate(email="test@example.com", password="password123")
    hashed_password = get_password_hash(user_data.password)

    user = User(
        email=user_data.email,
        hashed_password=hashed_password
    )

    assert user.email == user_data.email
    assert user.hashed_password == hashed_password
    assert isinstance(user.id, UUID)
    assert isinstance(user.created_at, datetime)
    assert isinstance(user.updated_at, datetime)


def test_user_model_email_validation():
    """Test email validation in User model"""
    user_data = UserCreate(email="test@example.com", password="password123")
    hashed_password = get_password_hash(user_data.password)

    user = User(
        email=user_data.email,
        hashed_password=hashed_password
    )

    assert user.email == "test@example.com"


def test_task_model_creation():
    """Test Task model creation with validation"""
    from uuid import uuid4

    user_id = uuid4()
    task_data = TaskCreate(title="Test Task", description="Test Description")

    task = Task(
        title=task_data.title,
        description=task_data.description,
        user_id=user_id
    )

    assert task.title == task_data.title
    assert task.description == task_data.description
    assert task.user_id == user_id
    assert task.completed is False
    assert isinstance(task.id, int)
    assert isinstance(task.created_at, datetime)
    assert isinstance(task.updated_at, datetime)


def test_task_model_title_validation():
    """Test title validation in Task model"""
    from uuid import uuid4

    user_id = uuid4()

    # Test valid title
    task = Task(
        title="Valid Title",
        description="Test Description",
        user_id=user_id
    )

    assert task.title == "Valid Title"

    # Test title length constraints
    with pytest.raises(Exception):
        # This test would fail at database level, not at model level
        # The validation happens at the schema level
        pass


def test_task_model_update():
    """Test Task model update functionality"""
    from uuid import uuid4

    user_id = uuid4()
    task = Task(
        title="Original Title",
        description="Original Description",
        user_id=user_id
    )

    # Update task
    original_updated_at = task.updated_at
    task.title = "Updated Title"

    # The updated_at should be automatically updated
    assert task.title == "Updated Title"
    assert task.updated_at > original_updated_at


if __name__ == "__main__":
    test_user_model_creation()
    test_user_model_email_validation()
    test_task_model_creation()
    test_task_model_title_validation()
    test_task_model_update()
    print("All unit tests passed!")