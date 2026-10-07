import pytest
from fastapi import HTTPException
from sqlalchemy import select


@pytest.fixture
def signed_in(client):
    for username in ["kea", "other"]:
        response = client.post("/users/register", json={"username": username, "email": f"{username}@example.com", "first_name": username.title(), "last_name": "Original", "password": "a-long-password"})
        assert response.status_code == 201
    assert client.post("/users/login", json={"username": "kea", "password": "a-long-password"}).status_code == 200
    return client


def test_profile_requires_authentication(client):
    assert client.patch("/users/me", json={"first_name": "Changed"}).status_code == 401


def test_profile_updates_only_the_signed_in_account_and_preserves_password(signed_in):
    from app.db.models.user import User

    with signed_in.sessions() as db:
        before = db.scalar(select(User).where(User.username == "kea")).hashed_password
    response = signed_in.patch("/users/me", json={"username": "kea-new", "email": "new@example.com", "first_name": "New", "last_name": "Name"})
    assert response.status_code == 200, response.text
    assert response.json()["first_name"] == "New"
    assert "password" not in response.text
    assert signed_in.get("/users/me").json()["email"] == "new@example.com"
    with signed_in.sessions() as db:
        assert db.scalar(select(User).where(User.username == "kea-new")).hashed_password == before
        assert db.scalar(select(User).where(User.username == "other")).first_name == "Other"
    signed_in.post("/users/logout")
    assert signed_in.post("/users/login", json={"username": "kea-new", "password": "a-long-password"}).status_code == 200


def test_partial_and_unchanged_profile_updates_keep_other_fields(signed_in):
    response = signed_in.patch("/users/me", json={"first_name": "  New  "})
    assert response.status_code == 200
    assert response.json()["first_name"] == "New"
    assert response.json()["last_name"] == "Original"
    assert response.json()["email"] == "kea@example.com"
    assert signed_in.patch("/users/me", json={"username": "kea", "email": "kea@example.com"}).status_code == 200


@pytest.mark.parametrize("changes", [{"username": "other"}, {"email": "other@example.com"}])
def test_duplicate_profile_fields_do_not_change_account(signed_in, changes):
    response = signed_in.patch("/users/me", json={"first_name": "Uncommitted", **changes})
    assert response.status_code == 400
    assert signed_in.get("/users/me").json()["first_name"] == "Kea"


@pytest.mark.parametrize("changes", [{"first_name": None}, {"last_name": " "}, {"username": "ab"}, {"email": "bad"}, {"first_name": "x" * 51}, {"is_admin": True}, {"is_active": False}, {"id": 2}, {"password": "new-password"}])
def test_profile_rejects_invalid_and_protected_fields(signed_in, changes):
    assert signed_in.patch("/users/me", json=changes).status_code == 422
    assert signed_in.get("/users/me").json()["username"] == "kea"


def test_profile_rejects_cross_origin_updates(signed_in):
    response = signed_in.patch("/users/me", json={"first_name": "Changed"}, headers={"Origin": "https://attacker.example"})
    assert response.status_code == 403
    assert signed_in.get("/users/me").json()["first_name"] == "Kea"


def test_profile_constraint_race_rolls_back_and_returns_safe_error(signed_in, monkeypatch):
    from app.db.models.user import User
    from app.db.repositories.user_repository import UserRepository
    from app.schemas.user import UserUpdate
    from app.services.user_service import UserService

    with signed_in.sessions() as db:
        user_id = db.scalar(select(User).where(User.username == "kea")).id
        repo = UserRepository(db)
        # Simulate a competing request taking the email after the pre-check.
        monkeypatch.setattr(repo, "get_user_by_email", lambda email: None)
        service = UserService(repo)
        with pytest.raises(HTTPException) as exc:
            service.update_user(user_id, UserUpdate(email="other@example.com"))
        assert exc.value.status_code == 400
        assert "UPDATE" not in exc.value.detail
        assert service.update_user(user_id, UserUpdate(first_name="Recovered")).first_name == "Recovered"
