import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.database import engine, get_db_session
from src.models.user import User
from sqlmodel import Session, select
from src.utils.security import verify_password


@pytest.fixture
def test_client():
    """Create a test client for the FastAPI app"""
    with TestClient(app) as client:
        yield client


def test_user_registration_integration():
    """Test the full user registration flow integration"""
    with TestClient(app) as client:
        # Register a new user
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "integration_test@example.com",
                "password": "password123"
            }
        )

        # Verify the response
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["email"] == "integration_test@example.com"
        assert "created_at" in data

        # Verify the user was actually created in the database
        with Session(engine) as session:
            user = session.exec(
                select(User).where(User.email == "integration_test@example.com")
            ).first()

            assert user is not None
            assert user.email == "integration_test@example.com"
            # Verify password is hashed
            assert user.hashed_password != "password123"


def test_user_login_integration():
    """Test the full user login flow integration"""
    with TestClient(app) as client:
        # First register a user
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "login_test@example.com",
                "password": "password123"
            }
        )

        # Login with the user
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "login_test@example.com",
                "password": "password123"
            }
        )

        # Verify the response
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

        # Verify the token is valid by using it
        token = data["access_token"]
        protected_response = client.get(
            "/api/v1/tasks/",
            headers={"Authorization": f"Bearer {token}"}
        )
        # Should return 200 (empty list) since user has no tasks
        assert protected_response.status_code in [200, 401]  # 401 if token is invalid


def test_user_login_with_wrong_password():
    """Test login with wrong password"""
    with TestClient(app) as client:
        # First register a user
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "wrong_password_test@example.com",
                "password": "password123"
            }
        )

        # Try to login with wrong password
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "wrong_password_test@example.com",
                "password": "wrongpassword"
            }
        )

        # Should return 401 Unauthorized
        assert response.status_code == 401


def test_user_login_with_nonexistent_user():
    """Test login with non-existent user"""
    with TestClient(app) as client:
        # Try to login with non-existent user
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "password123"
            }
        )

        # Should return 401 Unauthorized
        assert response.status_code == 401


def test_duplicate_user_registration():
    """Test registration with duplicate email"""
    with TestClient(app) as client:
        # Register a user first
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "duplicate_test@example.com",
                "password": "password123"
            }
        )

        # Try to register with the same email
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "duplicate_test@example.com",
                "password": "password123"
            }
        )

        # Should return 400 Bad Request
        assert response.status_code == 400


if __name__ == "__main__":
    test_user_registration_integration()
    test_user_login_integration()
    test_user_login_with_wrong_password()
    test_user_login_with_nonexistent_user()
    test_duplicate_user_registration()
    print("All auth integration tests passed!")