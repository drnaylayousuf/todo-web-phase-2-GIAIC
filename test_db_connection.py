#!/usr/bin/env python3
"""
Test script to verify database connection and table creation
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

from src.database import engine, create_db_and_tables
from src.models.user import User
from sqlmodel import select
from src.config import settings
from sqlmodel import Session

def test_db_connection():
    print(f"Database URL: {settings.database_url}")
    print("Attempting to create database tables...")

    try:
        create_db_and_tables()
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Error creating tables: {e}")
        return False

    print("Attempting to connect to database...")

    try:
        with Session(engine) as session:
            print("Connected to database successfully!")

            # Try to query users table
            try:
                statement = select(User)
                results = session.exec(statement)
                users = results.all()
                print(f"Found {len(users)} users in the database")

                for user in users[:5]:  # Show first 5 users
                    print(f"  - User ID: {user.id}, Email: {user.email}")

            except Exception as e:
                print(f"Error querying users table: {e}")
                return False

    except Exception as e:
        print(f"Error connecting to database: {e}")
        return False

    return True

if __name__ == "__main__":
    success = test_db_connection()
    if success:
        print("\n[SUCCESS] Database connection test passed!")
    else:
        print("\n[ERROR] Database connection test failed!")