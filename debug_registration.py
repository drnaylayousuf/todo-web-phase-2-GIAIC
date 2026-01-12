#!/usr/bin/env python3
"""
Detailed test script to debug user registration
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

from src.database import engine, create_db_and_tables
from src.models.user import User, UserCreate
from src.services.user_service import UserService
from src.utils.security import get_password_hash
from sqlmodel import Session, select
from src.config import settings
import traceback

def test_registration_detailed():
    print(f"Database URL: {settings.database_url}")
    print("Creating database tables...")

    try:
        create_db_and_tables()
        print("Tables created successfully")
    except Exception as e:
        print(f"Error creating tables: {e}")
        traceback.print_exc()
        return False

    print("\nAttempting to register a new user...")

    # Create user data
    user_data = UserCreate(email="debug_test@example.com", password="password123")

    try:
        with Session(engine) as session:
            print(f"Session created, attempting to register: {user_data.email}")

            # Check if user already exists
            existing_user = session.exec(select(User).where(User.email == user_data.email)).first()
            if existing_user:
                print(f"User {user_data.email} already exists, trying to delete first...")
                session.delete(existing_user)
                session.commit()
                print("Deleted existing user")

            # Try to create the user using the service
            try:
                user = UserService.create_user(session, user_data)
                print(f"✅ Successfully created user: {user.email}, ID: {user.id}")

                # Verify the user was actually created in the database
                created_user = session.exec(select(User).where(User.email == user_data.email)).first()
                if created_user:
                    print(f"✅ User verified in database: {created_user.email}")
                    return True
                else:
                    print("❌ User not found in database after creation")
                    return False

            except Exception as e:
                print(f"❌ Error in UserService.create_user: {e}")
                traceback.print_exc()
                return False

    except Exception as e:
        print(f"❌ Error in database session: {e}")
        traceback.print_exc()
        return False

def test_manual_creation():
    print("\n" + "="*50)
    print("TESTING MANUAL USER CREATION")
    print("="*50)

    try:
        with Session(engine) as session:
            # Manual creation test
            hashed_password = get_password_hash("password123")
            new_user = User(email="manual_test@example.com", hashed_password=hashed_password)

            print(f"Creating user object: {new_user.email}")

            session.add(new_user)
            session.commit()
            session.refresh(new_user)

            print(f"✅ Manual creation successful: {new_user.email}, ID: {new_user.id}")
            return True

    except Exception as e:
        print(f"❌ Manual creation failed: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Starting detailed registration debugging...")

    success1 = test_registration_detailed()
    success2 = test_manual_creation()

    if success1 and success2:
        print("\n[SUCCESS] All tests passed!")
    else:
        print("\n[ERROR] Some tests failed!")