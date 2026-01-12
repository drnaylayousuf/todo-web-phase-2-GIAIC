#!/usr/bin/env python3
"""
Test the API endpoints directly to identify the issue
"""

import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

from fastapi.testclient import TestClient
from src.main import create_app
from src.models.user import UserCreate

def test_api_endpoints():
    # Create a test client for the app
    app = create_app()
    client = TestClient(app)

    print("Testing API endpoints directly...")

    # Test the registration endpoint
    print("\n1. Testing registration endpoint:")
    response = client.post(
        "/api/auth/register",
        json={"email": "test_api@example.com", "password": "password123"}
    )
    print(f"   Status Code: {response.status_code}")
    print(f"   Response: {response.json()}")

    # Check if it's a validation error
    if response.status_code == 422:
        print("   This is a validation error - checking details...")
        try:
            details = response.json()
            print(f"   Error details: {details}")
        except:
            print("   Could not parse error details")

    # Test the login endpoint
    print("\n2. Testing login endpoint:")
    response = client.post(
        "/api/auth/login",
        json={"email": "test@example.com", "password": "password123"}
    )
    print(f"   Status Code: {response.status_code}")
    print(f"   Response: {response.json()}")

    # Test the root endpoint
    print("\n3. Testing root endpoint:")
    response = client.get("/")
    print(f"   Status Code: {response.status_code}")
    print(f"   Response: {response.json()}")

    # Test the health endpoint
    print("\n4. Testing health endpoint:")
    response = client.get("/health")
    print(f"   Status Code: {response.status_code}")
    print(f"   Response: {response.json()}")

if __name__ == "__main__":
    test_api_endpoints()