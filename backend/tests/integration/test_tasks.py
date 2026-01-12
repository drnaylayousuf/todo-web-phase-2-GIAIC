import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.database import engine, get_db_session
from src.models.user import User
from src.models.task import Task
from src.utils.security import create_access_token
from sqlmodel import Session, select
from uuid import uuid4


@pytest.fixture
def test_client():
    """Create a test client for the FastAPI app"""
    with TestClient(app) as client:
        yield client


def test_task_creation_integration():
    """Test the full task creation flow integration"""
    with TestClient(app) as client:
        # First register and login
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "task_integration_test@example.com",
                "password": "password123"
            }
        )

        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "task_integration_test@example.com",
                "password": "password123"
            }
        )

        token = login_response.json()["access_token"]

        # Create a task
        response = client.post(
            "/api/v1/tasks/",
            json={
                "title": "Integration Test Task",
                "description": "This is a test task for integration testing"
            },
            headers={"Authorization": f"Bearer {token}"}
        )

        # Verify the response
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Integration Test Task"
        assert data["description"] == "This is a test task for integration testing"
        assert data["completed"] is False

        # Verify the task was actually created in the database
        with Session(engine) as session:
            task = session.get(Task, data["id"])
            assert task is not None
            assert task.title == "Integration Test Task"
            assert task.description == "This is a test task for integration testing"
            assert task.completed is False


def test_task_list_integration():
    """Test the full task listing flow integration"""
    with TestClient(app) as client:
        # First register and login
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "task_list_test@example.com",
                "password": "password123"
            }
        )

        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "task_list_test@example.com",
                "password": "password123"
            }
        )

        token = login_response.json()["access_token"]

        # Create a task first
        client.post(
            "/api/v1/tasks/",
            json={
                "title": "List Test Task",
                "description": "Test task for listing"
            },
            headers={"Authorization": f"Bearer {token}"}
        )

        # Get the task list
        response = client.get(
            "/api/v1/tasks/",
            headers={"Authorization": f"Bearer {token}"}
        )

        # Verify the response
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

        # Check that our task is in the list
        task_found = False
        for task in data:
            if task["title"] == "List Test Task":
                task_found = True
                break
        assert task_found


def test_task_update_integration():
    """Test the full task update flow integration"""
    with TestClient(app) as client:
        # First register and login
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "task_update_test@example.com",
                "password": "password123"
            }
        )

        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "task_update_test@example.com",
                "password": "password123"
            }
        )

        token = login_response.json()["access_token"]

        # Create a task first
        create_response = client.post(
            "/api/v1/tasks/",
            json={
                "title": "Original Task",
                "description": "Original Description"
            },
            headers={"Authorization": f"Bearer {token}"}
        )

        task_id = create_response.json()["id"]

        # Update the task
        response = client.put(
            f"/api/v1/tasks/{task_id}",
            json={
                "title": "Updated Task",
                "description": "Updated Description"
            },
            headers={"Authorization": f"Bearer {token}"}
        )

        # Verify the response
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Task"
        assert data["description"] == "Updated Description"

        # Verify the task was actually updated in the database
        with Session(engine) as session:
            task = session.get(Task, task_id)
            assert task is not None
            assert task.title == "Updated Task"
            assert task.description == "Updated Description"


def test_task_completion_toggle_integration():
    """Test the full task completion toggle flow integration"""
    with TestClient(app) as client:
        # First register and login
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "task_toggle_test@example.com",
                "password": "password123"
            }
        )

        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "task_toggle_test@example.com",
                "password": "password123"
            }
        )

        token = login_response.json()["access_token"]

        # Create a task first
        create_response = client.post(
            "/api/v1/tasks/",
            json={
                "title": "Toggle Test Task",
                "description": "Test task for toggling completion"
            },
            headers={"Authorization": f"Bearer {token}"}
        )

        task_id = create_response.json()["id"]

        # Toggle the task completion
        response = client.patch(
            f"/api/v1/tasks/{task_id}/toggle",
            headers={"Authorization": f"Bearer {token}"}
        )

        # Verify the response
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == task_id
        assert data["completed"] is True  # Initially false, now should be true

        # Verify the task was actually updated in the database
        with Session(engine) as session:
            task = session.get(Task, task_id)
            assert task is not None
            assert task.completed is True


def test_task_deletion_integration():
    """Test the full task deletion flow integration"""
    with TestClient(app) as client:
        # First register and login
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "task_delete_test@example.com",
                "password": "password123"
            }
        )

        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "task_delete_test@example.com",
                "password": "password123"
            }
        )

        token = login_response.json()["access_token"]

        # Create a task first
        create_response = client.post(
            "/api/v1/tasks/",
            json={
                "title": "Delete Test Task",
                "description": "Test task for deletion"
            },
            headers={"Authorization": f"Bearer {token}"}
        )

        task_id = create_response.json()["id"]

        # Verify the task exists before deletion
        with Session(engine) as session:
            task = session.get(Task, task_id)
            assert task is not None

        # Delete the task
        response = client.delete(
            f"/api/v1/tasks/{task_id}",
            headers={"Authorization": f"Bearer {token}"}
        )

        # Verify the response
        assert response.status_code == 200

        # Verify the task was actually deleted from the database
        with Session(engine) as session:
            task = session.get(Task, task_id)
            assert task is None


def test_user_isolation_integration():
    """Test that users can only access their own tasks"""
    with TestClient(app) as client:
        # Register first user
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "user1@example.com",
                "password": "password123"
            }
        )
        login1_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "user1@example.com",
                "password": "password123"
            }
        )
        token1 = login1_response.json()["access_token"]

        # Register second user
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "user2@example.com",
                "password": "password123"
            }
        )
        login2_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "user2@example.com",
                "password": "password123"
            }
        )
        token2 = login2_response.json()["access_token"]

        # Create a task for user1
        task1_response = client.post(
            "/api/v1/tasks/",
            json={
                "title": "User1's Task",
                "description": "Task for user 1"
            },
            headers={"Authorization": f"Bearer {token1}"}
        )
        task1_id = task1_response.json()["id"]

        # Create a task for user2
        task2_response = client.post(
            "/api/v1/tasks/",
            json={
                "title": "User2's Task",
                "description": "Task for user 2"
            },
            headers={"Authorization": f"Bearer {token2}"}
        )
        task2_id = task2_response.json()["id"]

        # User1 should only see their own task
        user1_tasks_response = client.get(
            "/api/v1/tasks/",
            headers={"Authorization": f"Bearer {token1}"}
        )
        user1_tasks = user1_tasks_response.json()
        user1_task_ids = [task["id"] for task in user1_tasks]
        assert task1_id in user1_task_ids
        assert task2_id not in user1_task_ids

        # User2 should only see their own task
        user2_tasks_response = client.get(
            "/api/v1/tasks/",
            headers={"Authorization": f"Bearer {token2}"}
        )
        user2_tasks = user2_tasks_response.json()
        user2_task_ids = [task["id"] for task in user2_tasks]
        assert task2_id in user2_task_ids
        assert task1_id not in user2_task_ids

        # User1 should not be able to access user2's task directly
        task2_response_user1 = client.get(
            f"/api/v1/tasks/{task2_id}",
            headers={"Authorization": f"Bearer {token1}"}
        )
        # Should return 404 since user1 doesn't own task2
        assert task2_response_user1.status_code in [404, 401]


if __name__ == "__main__":
    test_task_creation_integration()
    test_task_list_integration()
    test_task_update_integration()
    test_task_completion_toggle_integration()
    test_task_deletion_integration()
    test_user_isolation_integration()
    print("All tasks integration tests passed!")