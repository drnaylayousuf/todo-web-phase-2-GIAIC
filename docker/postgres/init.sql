-- PostgreSQL initialization script for task app

-- Create the database (this is actually done by the POSTGRES_DB environment variable)
-- CREATE DATABASE task_app;

-- Create the user table (SQLModel will handle this via Alembic migrations in production)
-- For now, we just ensure the database is ready to accept connections

-- You can add any additional initialization SQL here
-- For example, extensions:
-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- The actual table creation will be handled by Alembic migrations when the app starts