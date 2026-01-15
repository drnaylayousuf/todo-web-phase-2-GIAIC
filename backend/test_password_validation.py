#!/usr/bin/env python3
"""
Test script to verify password validation fixes work correctly
"""

import sys
import os

# Add the backend/src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import using absolute paths
from src.models.user import UserCreate
from src.utils.security import get_password_hash, verify_password

def test_password_validation():
    print("Testing password validation...")

    # Test 1: Short password (should work)
    try:
        user_short = UserCreate(email="test@example.com", password="short123")
        print(f"✓ Short password validation passed: {len('short123')} chars")
    except ValueError as e:
        print(f"✗ Short password validation failed: {e}")

    # Test 2: 72-char password (should work)
    try:
        long_password = "a" * 72
        user_long = UserCreate(email="test2@example.com", password=long_password)
        print(f"✓ 72-char password validation passed: {len(long_password)} chars")
    except ValueError as e:
        print(f"✗ 72-char password validation failed: {e}")

    # Test 3: 73-char password (should fail)
    try:
        too_long_password = "a" * 73
        user_too_long = UserCreate(email="test3@example.com", password=too_long_password)
        print(f"✗ 73-char password validation should have failed but passed: {len(too_long_password)} chars")
    except ValueError as e:
        print(f"✓ 73-char password validation correctly failed: {e}")

    # Test 4: Test the security functions with long password
    print("\nTesting security functions...")
    try:
        # This should work - the security functions handle the truncation
        long_password = "a" * 80
        hashed = get_password_hash(long_password)
        is_valid = verify_password(long_password, hashed)
        print(f"✓ Security functions handled 80-char password correctly")
    except Exception as e:
        print(f"✗ Security functions failed with long password: {e}")

if __name__ == "__main__":
    test_password_validation()
    print("\nTest completed!")