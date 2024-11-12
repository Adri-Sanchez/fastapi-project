import os
import jwt
from typing import Annotated
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

from db import engine
from .models import User, Role

# OAuth2 password bearer for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
OAuthDep = Annotated[str, Depends(oauth2_scheme)]

# Password context for hashing and verification
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Secret key for JWT encoding and decoding
SECRET_KEY = os.getenv("SECRET_KEY", "secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5


def verify_password(plain_password, hashed_password):
    """Verify that a plain password matches the hashed password.

    Args:
        plain_password (str): The plain text password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the passwords match, otherwise False.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """Generate a hashed version of the password.

    Args:
        password (str): The plain text password to hash.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expire_delta: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    """Create a JWT access token with an expiration time.

    Args:
        data (dict): The payload data to encode in the token.
        expire_delta (int): The expiration time in minutes (default is 5 minutes).

    Returns:
        str: The encoded JWT access token.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expire_delta)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: OAuthDep):
    """Retrieve the current user from the database based on the provided token.

    Args:
        token (str): The JWT token for user authentication.

    Raises:
        HTTPException: If the token is invalid or the user cannot be found.

    Returns:
        User: The user object corresponding to the token's username.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    # Retrieve the user from the database
    with Session(engine) as session:
        user = session.query(User).filter(User.username == username).first()

    if user is None:
        raise credentials_exception

    return user


async def role_required(current_user: Annotated[User, Depends(get_current_user)], required_role: Role):
    """Check if the current user has the required role.

    Args:
        current_user (User): The current authenticated user.
        required_role (Role): The required role for access.

    Raises:
        HTTPException: If the user does not have the required role.

    Returns:
        User: The current user if the role matches the required role.
    """
    if not current_user or current_user.role != required_role:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"{required_role} required")
    return current_user


async def admin_required(current_user: Annotated[User, Depends(get_current_user)]):
    """Ensure the current user is an admin.

    Args:
        current_user (User): The current authenticated user.

    Returns:
        User: The current user if they are an admin.
    """
    return await role_required(current_user, Role.ADMIN)


async def user_required(current_user: Annotated[User, Depends(get_current_user)]):
    """Ensure the current user is a regular user.

    Args:
        current_user (User): The current authenticated user.

    Returns:
        User: The current user if they are a regular user.
    """
    return await role_required(current_user, Role.USER)


def initialize_admin_user():
    """Initialize the admin user if none exists
    """
    with Session(engine) as session:
        user = session.query(User).filter(User.role == Role.ADMIN).first()

        if not user:
            username = os.getenv("ADMIN_USERNAME", "admin")
            password = os.getenv("ADMIN_PASSWORD", "password")
            hashed_password = get_password_hash(password)
            user = User(username=username, hashed_password=hashed_password, role=Role.ADMIN)
            session.add(user)
            session.commit()


# Dependency aliases for user roles
UserRequired = Annotated[User, Depends(user_required)]
AdminRequired = Annotated[User, Depends(admin_required)]
