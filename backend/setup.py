from setuptools import setup, find_packages

setup(
    name='task-crud-backend',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'fastapi>=0.115.0',
        'uvicorn>=0.32.0',
        'sqlmodel>=0.0.22',
        'pydantic>=2.9.0',
        'python-multipart>=0.0.20',
        'bcrypt>=4.2.0',
        'python-jose[cryptography]>=3.3.0',
        'passlib[bcrypt]>=1.7.4',
        'better-exceptions>=0.3.3',
        'psycopg2-binary>=2.9.10',
        'alembic>=1.13.3',
        'python-dotenv>=1.0.1',
        'pydantic-settings>=2.6.0',
    ],
)