from fastapi import HTTPException
from sqlmodel import Session

from .models import UserRequest, User
from .utils import get_password_hash


def create_user(user: UserRequest, session: Session):
    """Create a new user in the database.

    Args:
        user (UserRequest): The user data containing the username and password.
        session (Session): The SQLModel database session to interact with the database.

    Returns:
        dict: A dictionary containing a success message and the new user's ID.

    Raises:
        HTTPException: If an error occurs while creating the user, a 400 error is raised.
    """
    try:
        hashed_password = get_password_hash(user.password)
        new_user = User(username=user.username, hashed_password=hashed_password)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)  # Refresh to get the latest data
        return {"message": "User created successfully", "user_id": new_user.id}
    except Exception as e:
        session.rollback()  # Rollback if error occurs
        raise HTTPException(status_code=400, detail="Error creating user")
