import os
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

# Database configuration
database_url = os.getenv("DATABASE_URL")
engine = create_engine(database_url)


def create_db_and_tables():
    """
    Creates the database and tables defined in the SQLModel metadata.

    Returns:
        None
    """
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Yields a database session for use in database operations.

    Yields:
        Session: A database session object.
    """
    with Session(engine) as session:
        yield session


# Dependency for injecting a database session into routes or functions
SessionDep = Annotated[Session, Depends(get_session)]
