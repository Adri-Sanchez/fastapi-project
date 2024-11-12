from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from db import SessionDep
from .utils import get_current_user, admin_required, create_access_token, verify_password
from .models import User, UserRequest, Token
from .user_crud import create_user

auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication Endpoints"],
)


@auth_router.post("/users/create", dependencies=[Depends(admin_required)])
async def create_new_user(
        user: UserRequest,
        session: SessionDep,
):
    """Create a new user. Restricted to Admin users.

    Args:
        user (UserRequest): The user data for creating the new user.
        session (SessionDep): The database session dependency.

    Returns:
        User: The created user object.
    """
    return create_user(user, session)


@auth_router.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    """Retrieve the current authenticated user's data.

    Args:
        current_user (User): The current authenticated user.

    Returns:
        User: The current authenticated user's data.
    """
    return current_user


@auth_router.post("/token")
async def login(session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    """Generate and return an access token for the user.

    Args:
        session (SessionDep): The database session dependency.
        form_data (OAuth2PasswordRequestForm): The username and password submitted by the user.

    Raises:
        HTTPException: If the credentials are incorrect, an unauthorized error is raised.

    Returns:
        Token: The generated access token and its type.
    """
    user = session.query(User).filter(User.username == form_data.username).first()

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})

    return Token(access_token=access_token, token_type="bearer")
