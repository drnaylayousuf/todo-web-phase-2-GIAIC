from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlmodel import Session
from datetime import timedelta
import logging
from ..database import get_db_session
from ..models.user import UserCreate
from ..schemas.user import UserLogin, Token
from ..services.user_service import UserService
from ..utils.security import create_access_token
from ..config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_create: UserCreate, db_session: Session = Depends(get_db_session)):
    """Register a new user"""
    try:
        user = UserService.create_user(db_session, user_create)

        # Return success response without password
        return {
            "id": user.id,
            "email": user.email,
            "created_at": user.created_at
        }
    except ValueError as e:
        logger.error(f"Registration error for email {user_create.email}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected registration error for email {user_create.email}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during registration"
        )


@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin, db_session: Session = Depends(get_db_session)):
    """Authenticate user and return access token"""
    logger.info(f"Login attempt for email: {user_credentials.email}")

    try:
        user = UserService.authenticate_user(
            db_session,
            user_credentials.email,
            user_credentials.password
        )

        if not user:
            logger.warning(f"Failed login attempt for email: {user_credentials.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create access token
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )

        logger.info(f"Successful login for user ID: {user.id}")
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        logger.error(f"Unexpected error during login for email {user_credentials.email}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during login"
        )