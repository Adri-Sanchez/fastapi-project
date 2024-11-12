import jwt
from fastapi import status
from fastapi.testclient import TestClient

from sqlmodel import Session
from auth.models import User
from auth.utils import SECRET_KEY, create_access_token


def test_create_user(client: TestClient, session: Session, admin_token: str):
    # Make the request
    username = "Bob"
    response = client.post(
        "/auth/users/create",
        json={"username": username, "password": "new_password"},
        headers={"Authorization": f"Bearer {admin_token}"}  # Pass the token in the Authorization header
    )

    # Assert the response
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "User created successfully"

    # Retrieve the created user from the database
    user = session.query(User).filter(User.username == username).first()
    assert user


def test_create_user_duplicate_username(client: TestClient, admin_token: str):
    # Test duplicate username error
    username = "Alice"
    response = client.post(
        "/auth/users/create",
        json={"username": username, "password": "new_password"},
        headers={"Authorization": f"Bearer {admin_token}"}  # Pass the token in the Authorization header
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Error creating user"


def test_create_access_token():
    # Test access token creation
    token_data = {"sub": "Alice"}
    token = create_access_token(data=token_data, expire_delta=10)
    decoded_data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    assert decoded_data["sub"] == "Alice"


def test_get_current_user(client: TestClient, session: Session):
    # Test retrieving the current user
    username = "Alice"
    token = create_access_token(data={"sub": username})
    response = client.get("/auth/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == username
