#!/usr/bin/env python3
"""
Simple test to verify password validation works correctly
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import only what we need for validation testing
from pydantic import ValidationError
from src.models.user import UserCreate

def test_password_validation():
    print("Testing password validation...")

    # Test 1: Short password (should work)
    try:
        user_short = UserCreate(email="test@example.com", password="short123")
        print(f"[PASS] Short password validation passed: {len('short123')} chars")
    except ValueError as e:
        print(f"[FAIL] Short password validation failed: {e}")

    # Test 2: 72-char password (should work)
    try:
        long_password = "a" * 72
        user_long = UserCreate(email="test2@example.com", password=long_password)
        print(f"[PASS] 72-char password validation passed: {len(long_password)} chars")
    except ValueError as e:
        print(f"[FAIL] 72-char password validation failed: {e}")

    # Test 3: 73-char password (should fail)
    try:
        too_long_password = "a" * 73
        user_too_long = UserCreate(email="test3@example.com", password=too_long_password)
        print(f"[FAIL] 73-char password validation should have failed but passed: {len(too_long_password)} chars")
    except ValueError as e:
        print(f"[PASS] 73-char password validation correctly failed: {e}")

    # Test 4: Very long password (should fail)
    try:
        very_long_password = "a" * 100
        user_very_long = UserCreate(email="test4@example.com", password=very_long_password)
        print(f"[FAIL] 100-char password validation should have failed but passed: {len(very_long_password)} chars")
    except ValueError as e:
        print(f"[PASS] 100-char password validation correctly failed: {e}")

    print("\nAll validation tests completed!")

if __name__ == "__main__":
    test_password_validation()