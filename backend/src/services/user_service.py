from sqlmodel import Session, select
from typing import Optional
from uuid import UUID
import logging
from ..models.user import User, UserCreate
from ..utils.security import get_password_hash, verify_password


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UserService:
    @staticmethod
    def create_user(db_session: Session, user_create: UserCreate) -> User:
        """Create a new user with hashed password"""
        logger.info(f"Starting user registration for email: {user_create.email}")

        # Check if user with this email already exists
        existing_user = db_session.exec(
            select(User).where(User.email == user_create.email)
        ).first()

        if existing_user:
            logger.warning(f"Registration attempt with existing email: {user_create.email}")
            raise ValueError("An account with this email already exists")

        # Hash the password
        hashed_password = get_password_hash(user_create.password)

        # Create the user
        db_user = User(
            email=user_create.email,
            hashed_password=hashed_password
        )

        db_session.add(db_user)
        db_session.commit()
        db_session.refresh(db_user)

        logger.info(f"Successfully created user with ID: {db_user.id}")

        return db_user

    @staticmethod
    def authenticate_user(db_session: Session, email: str, password: str) -> Optional[User]:
        """Authenticate a user by email and password"""
        logger.info(f"Authentication attempt for email: {email}")

        user = db_session.exec(
            select(User).where(User.email == email)
        ).first()

        if not user or not verify_password(password, user.hashed_password):
            logger.warning(f"Failed authentication attempt for email: {email}")
            return None

        logger.info(f"Successful authentication for user ID: {user.id}")
        return user

    @staticmethod
    def get_user_by_id(db_session: Session, user_id: UUID) -> Optional[User]:
        """Get a user by their ID"""
        logger.info(f"Retrieving user by ID: {user_id}")
        user = db_session.get(User, user_id)
        if user:
            logger.info(f"Successfully retrieved user: {user.id}")
        else:
            logger.warning(f"User not found for ID: {user_id}")
        return user