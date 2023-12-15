from unittest.mock import patch

import pytest
from src.database.models import User, Role
from src.conf import messages
from src.schemas import AllUsersProfiles, UserProfileMe
from src.services.auth import auth_service


@pytest.fixture()
def token(client, user, session):
    client.post("/project/auth/signup", json=user)

    current_user: User = (
        session.query(User).filter(User.email == user.get("email")).first()
    )

    response = client.post(
        "/project/auth/login",
        data={"username": user.get("email"), "password": user.get("password")},
    )
    data = response.json()
    return data["access_token"]


def test_user_me(user, session, client, token):
    with patch.object(auth_service, "redis_db") as redis_mock:
        redis_mock.get.return_value = None
        current_user: User = (
            session.query(User).filter(User.email == user.get("email")).first()
        )
        session.commit()
        response = client.get(
            "/project/users/me", headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        payload = response.json()
        assert type(payload["user"]) == dict


def test_users(user, session, client, token):
    with patch.object(auth_service, "redis_db") as redis_mock:
        redis_mock.get.return_value = None
        response = client.get(
            "/project/users", headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        payload = response.json()
        assert type(payload) == dict


def test_user_change_role(user, session, client, token):
    with patch.object(auth_service, "redis_db") as redis_mock:
        redis_mock.get.return_value = None
        client.post("/project/auth/signup", json={"name": "Dima", "email": "exam@exam.com", "password": "qwerty"})

        response = client.patch(
            "/project/users/user",
            json={"email": "exam@exam.com", "role": "moderator"},
            headers={"Authorization": f"Bearer {token}"},

        )
        assert response.status_code == 200, response.text
        payload = response.json()
        assert payload["name"] == "Dima"
        assert payload["email"] == "exam@exam.com"
        assert payload["role"] == "moderator"




