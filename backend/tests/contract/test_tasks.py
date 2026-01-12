import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.models.user import User
from src.models.task import Task
from src.utils.security import create_access_token
from uuid import uuid4
import json


@pytest.fixture
def test_client():
    """Create a test client for the FastAPI app"""
    with TestClient(app) as client:
        yield client


def test_task_creation_endpoint_contract():
    """Test task creation endpoint contract"""
    with TestClient(app) as client:
        # First register and login to get a token
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "password123"
            }
        )

        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "password123"
            }
        )

        token = login_response.json()["access_token"]

        # Create a task
        response = client.post(
            "/api/v1/tasks/",
            json={
                "title": "Test Task",
                "description": "Test Description"
            },
            headers={"Authorization": f"Bearer {token}"}
        )

        # Should return 201 Created
        assert response.status_code == 201

        # Should return task data
        data = response.json()
        assert "id" in data
        assert data["title"] == "Test Task"
        assert data["description"] == "Test Description"
        assert data["completed"] is False
        assert "user_id" in data
        assert "created_at" in data
        assert "updated_at" in data


def test_task_creation_endpoint_contract_missing_title():
    """Test task creation endpoint contract with missing title"""
    with TestClient(app) as client:
        # First register and login to get a token
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "password123"
            }
        )

        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "password123"
            }
        )

        token = login_response.json()["access_token"]

        # Try to create a task without title
        response = client.post(
            "/api/v1/tasks/",
            json={
                "description": "Test Description"
            },
            headers={"Authorization": f"Bearer {token}"}
        )

        # Should return 422 Unprocessable Entity (validation error)
        assert response.status_code == 422


def test_task_list_endpoint_contract():
    """Test task list endpoint contract"""
    with TestClient(app) as client:
        # First register and login to get a token
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "password123"
            }
        )

        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "password123"
            }
        )

        token = login_response.json()["access_token"]

        # Create a task first
        client.post(
            "/api/v1/tasks/",
            json={
                "title": "Test Task",
                "description": "Test Description"
            },
            headers={"Authorization": f"Bearer {token}"}
        )

        # Get tasks list
        response = client.get(
            "/api/v1/tasks/",
            headers={"Authorization": f"Bearer {token}"}
        )

        # Should return 200 OK
        assert response.status_code == 200

        # Should return a list
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

        # Check the structure of a task
        task = data[0]
        assert "id" in task
        assert "title" in task
        assert "description" in task
        assert "completed" in task
        assert "user_id" in task
        assert "created_at" in task
        assert "updated_at" in task


def test_task_update_endpoint_contract():
    """Test task update endpoint contract"""
    with TestClient(app) as client:
        # First register and login to get a token
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "password123"
            }
        )

        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "password123"
            }
        )

        token = login_response.json()["access_token"]

        # Create a task first
        create_response = client.post(
            "/api/v1/tasks/",
            json={
                "title": "Test Task",
                "description": "Test Description"
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

        # Should return 200 OK
        assert response.status_code == 200

        # Should return updated task data
        data = response.json()
        assert data["id"] == task_id
        assert data["title"] == "Updated Task"
        assert data["description"] == "Updated Description"


def test_task_completion_toggle_endpoint_contract():
    """Test task completion toggle endpoint contract"""
    with TestClient(app) as client:
        # First register and login to get a token
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "password123"
            }
        )

        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "password123"
            }
        )

        token = login_response.json()["access_token"]

        # Create a task first
        create_response = client.post(
            "/api/v1/tasks/",
            json={
                "title": "Test Task",
                "description": "Test Description"
            },
            headers={"Authorization": f"Bearer {token}"}
        )

        task_id = create_response.json()["id"]

        # Toggle task completion
        response = client.patch(
            f"/api/v1/tasks/{task_id}/toggle",
            headers={"Authorization": f"Bearer {token}"}
        )

        # Should return 200 OK
        assert response.status_code == 200

        # Should return updated task data
        data = response.json()
        assert data["id"] == task_id
        assert data["completed"] is True  # Initially false, now should be true


def test_task_deletion_endpoint_contract():
    """Test task deletion endpoint contract"""
    with TestClient(app) as client:
        # First register and login to get a token
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "password123"
            }
        )

        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "password123"
            }
        )

        token = login_response.json()["access_token"]

        # Create a task first
        create_response = client.post(
            "/api/v1/tasks/",
            json={
                "title": "Test Task",
                "description": "Test Description"
            },
            headers={"Authorization": f"Bearer {token}"}
        )

        task_id = create_response.json()["id"]

        # Delete the task
        response = client.delete(
            f"/api/v1/tasks/{task_id}",
            headers={"Authorization": f"Bearer {token}"}
        )

        # Should return 200 OK
        assert response.status_code == 200

        # Should return success message
        data = response.json()
        assert "message" in data
        assert "deleted" in data["message"]


if __name__ == "__main__":
    test_task_creation_endpoint_contract()
    test_task_creation_endpoint_contract_missing_title()
    test_task_list_endpoint_contract()
    test_task_update_endpoint_contract()
    test_task_completion_toggle_endpoint_contract()
    test_task_deletion_endpoint_contract()
    print("All tasks contract tests passed!")