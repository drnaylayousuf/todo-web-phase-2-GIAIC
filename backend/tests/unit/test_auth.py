import pytest
from src.utils.security import verify_password, get_password_hash, create_access_token, verify_token
from datetime import timedelta
from jose import jwt
from src.config import settings


def test_verify_password():
    """Test password verification"""
    plain_password = "testpassword"
    hashed_password = get_password_hash(plain_password)

    # Should return True for correct password
    assert verify_password(plain_password, hashed_password) is True

    # Should return False for wrong password
    assert verify_password("wrongpassword", hashed_password) is False


def test_get_password_hash():
    """Test password hashing"""
    plain_password = "testpassword"
    hashed_password = get_password_hash(plain_password)

    # Should not be equal to plain password
    assert plain_password != hashed_password

    # Should verify correctly
    assert verify_password(plain_password, hashed_password) is True


def test_create_access_token():
    """Test access token creation"""
    data = {"sub": "testuser"}
    expires_delta = timedelta(minutes=30)

    token = create_access_token(data=data, expires_delta=expires_delta)

    # Should be a string
    assert isinstance(token, str)

    # Should contain the data
    decoded_data = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    assert decoded_data["sub"] == "testuser"


def test_verify_token():
    """Test token verification"""
    data = {"sub": "testuser"}
    token = create_access_token(data=data)

    # Should verify correctly
    decoded_payload = verify_token(token)
    assert decoded_payload is not None
    assert decoded_payload["sub"] == "testuser"


def test_verify_token_invalid():
    """Test token verification with invalid token"""
    # Should return None for invalid token
    result = verify_token("invalid_token")
    assert result is None


def test_verify_token_expired():
    """Test token verification with expired token"""
    data = {"sub": "testuser"}
    # Create token that expires immediately
    expired_token = create_access_token(data=data, expires_delta=timedelta(seconds=1))

    # Wait for token to expire
    import time
    time.sleep(2)

    # Should return None for expired token
    result = verify_token(expired_token)
    assert result is None


if __name__ == "__main__":
    test_verify_password()
    test_get_password_hash()
    test_create_access_token()
    test_verify_token()
    test_verify_token_invalid()
    test_verify_token_expired()
    print("All auth unit tests passed!")