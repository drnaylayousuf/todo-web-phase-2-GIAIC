import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.database import engine, get_db_session
from sqlmodel import Session, SQLModel, create_engine
from contextlib import contextmanager
from unittest.mock import patch
import json


@pytest.fixture
def test_client():
    """Create a test client for the FastAPI app"""
    with TestClient(app) as client:
        yield client


def test_register_endpoint_contract():
    """Test registration endpoint contract"""
    with TestClient(app) as client:
        # Test valid registration
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "password123"
            }
        )

        # Should return 201 Created
        assert response.status_code == 201

        # Should return user data without password
        data = response.json()
        assert "id" in data
        assert data["email"] == "test@example.com"
        assert "created_at" in data

        # Should not return password
        assert "password" not in data
        assert "hashed_password" not in data


def test_register_endpoint_contract_invalid_email():
    """Test registration endpoint contract with invalid email"""
    with TestClient(app) as client:
        # Test invalid email
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "invalid-email",
                "password": "password123"
            }
        )

        # Should return 400 Bad Request
        assert response.status_code == 400

        # Should return error message
        data = response.json()
        assert "detail" in data


def test_register_endpoint_contract_weak_password():
    """Test registration endpoint contract with weak password"""
    with TestClient(app) as client:
        # Test weak password (less than 8 chars)
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "123"  # Too short
            }
        )

        # Should return 400 Bad Request
        assert response.status_code == 400

        # Should return error message
        data = response.json()
        assert "detail" in data


def test_login_endpoint_contract():
    """Test login endpoint contract"""
    with TestClient(app) as client:
        # First register a user
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "password123"
            }
        )

        # Then try to login
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "password123"
            }
        )

        # Should return 200 OK
        assert response.status_code == 200

        # Should return token data
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"


def test_login_endpoint_contract_invalid_credentials():
    """Test login endpoint contract with invalid credentials"""
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

        # Should return error message
        data = response.json()
        assert "detail" in data


if __name__ == "__main__":
    test_register_endpoint_contract()
    test_register_endpoint_contract_invalid_email()
    test_register_endpoint_contract_weak_password()
    test_login_endpoint_contract()
    test_login_endpoint_contract_invalid_credentials()
    print("All auth contract tests passed!")