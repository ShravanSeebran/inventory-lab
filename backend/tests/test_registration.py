import importlib

import pytest
from sqlalchemy import select


def test_application_can_start():
    try:
        importlib.import_module("app.main")
    except ImportError as exc:
        pytest.fail(f"The application must start: {exc}")


USER = {"username": "kea", "email": "kea@example.com", "first_name": "Kea", "last_name": "Nhlapo", "password": "a-long-password"}


def test_registration_persists_names_and_hashes_password(client):
    from app.db.models.user import User
    from app.services.user_service import verify_password

    response = client.post("/users/register", json=USER)
    assert response.status_code == 201, response.text
    assert response.json()["first_name"] == "Kea"
    assert "password" not in response.text
    with client.sessions() as db:
        user = db.scalar(select(User))
        assert user.last_name == "Nhlapo"
        assert user.is_active and not user.is_admin
        assert user.hashed_password != USER["password"]
        assert verify_password(USER["password"], user.hashed_password)


@pytest.mark.parametrize("field", ["email", "username"])
def test_registration_rejects_duplicates(client, field):
    assert client.post("/users/register", json=USER).status_code == 201
    other = {**USER, "username": "other", "email": "other@example.com", field: USER[field]}
    assert client.post("/users/register", json=other).status_code == 400


@pytest.mark.parametrize("changes", [{"username": " "}, {"email": "bad"}, {"password": "short"}, {"first_name": ""}, {"is_admin": True}, {"is_active": False}])
def test_registration_validates_public_fields(client, changes):
    assert client.post("/users/register", json={**USER, **changes}).status_code == 422


def test_registration_page_is_served(client):
    response = client.get("/register")
    assert response.status_code == 200
    assert 'text/html' in response.headers['content-type']
    assert '<form' in response.text
