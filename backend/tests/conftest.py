import os
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine, StaticPool

from main import app
from db import get_session
from auth.models import User, Role
from auth.utils import create_access_token

@pytest.fixture(scope="session", name="session")
def session_fixture():
    database_url = os.getenv("DATABASE_URL")
    engine = create_engine(
        database_url, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        user_1 = User(username="Alice", hashed_password="password")
        user_2 = User(username="admin", hashed_password="password", role="admin")
        session.add_all([user_1, user_2])
        session.commit()
        yield session
        SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(session: Session) -> User:
    return session.query(User).filter(User.role == Role.USER).first()


@pytest.fixture
def test_admin(session: Session) -> User:
    return session.query(User).filter(User.role == Role.ADMIN).first()

@pytest.fixture(name="admin_token")
def get_admin_token(test_admin: User) -> str:
    return create_access_token({"sub": test_admin.username})
