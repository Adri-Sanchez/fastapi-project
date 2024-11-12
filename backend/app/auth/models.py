from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from enum import Enum


class Role(str, Enum):
    """Enum representing user roles.

    Attributes:
        USER: Regular user role.
        ADMIN: Administrator role.
    """
    USER = "user"
    ADMIN = "admin"


class UserBase(SQLModel):
    """Base model for a user.

    Attributes:
        username (str): The username of the user.
    """
    username: str = Field(default=None, unique=True)


class UserRequest(UserBase):
    """Model for user registration or login requests.

    Inherits from UserBase and adds the password field.

    Attributes:
        password (str): The password provided by the user for authentication.
    """
    password: str


class User(UserBase, table=True):
    """Model representing a user in the database.

    Inherits from UserBase and adds additional fields for database storage.

    Attributes:
        id (int): The unique identifier for the user.
        hashed_password (str): The hashed password for authentication.
        role (Role): The role of the user (default is Role.USER).
    """
    id: int = Field(default=None, primary_key=True)
    hashed_password: str
    role: Role = Field(default=Role.USER)


class Token(BaseModel):
    """Model for a JWT token.

    Attributes:
        access_token (str): The JWT access token.
        token_type (str): The type of the token (e.g., 'bearer').
    """
    access_token: str
    token_type: str
