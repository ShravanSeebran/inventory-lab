from datetime import datetime, timedelta, UTC

import pytest
from sqlalchemy import select


@pytest.fixture
def account(client):
    data = {"username": "kea", "email": "kea@example.com", "first_name": "Kea", "last_name": "Nhlapo", "password": "a-long-password"}
    assert client.post("/users/register", json=data).status_code == 201
    return data


def sign_in(client, account):
    return client.post("/users/login", json={"username": account["username"], "password": account["password"]})


def test_login_establishes_private_session_and_logout_revokes_it(client, account):
    assert client.get("/users/me").status_code == 401
    response = sign_in(client, account)
    assert response.status_code == 200
    assert "password" not in response.text
    cookie = response.headers["set-cookie"]
    assert "httponly" in cookie.lower() and "samesite=lax" in cookie.lower()
    token = client.cookies.get("inventory_session")
    assert token
    assert client.get("/users/me").json()["username"] == "kea"
    assert client.post("/users/logout").status_code == 204
    assert client.get("/users/me").status_code == 401
    client.cookies.set("inventory_session", token)
    assert client.get("/users/me").status_code == 401


@pytest.mark.parametrize("username,password", [("kea", "wrong-password"), ("missing", "a-long-password")])
def test_invalid_credentials_do_not_set_session(client, account, username, password):
    response = client.post("/users/login", json={"username": username, "password": password})
    assert response.status_code == 401
    assert "set-cookie" not in response.headers


def test_inactive_users_cannot_login_or_reuse_session(client, account):
    from app.db.models.user import User

    sign_in(client, account)
    with client.sessions() as db:
        user = db.scalar(select(User))
        user.is_active = False
        db.commit()
    assert client.get("/users/me").status_code == 401
    assert sign_in(client, account).status_code == 401


def test_forged_and_expired_sessions_are_rejected(client, account):
    client.cookies.set("inventory_session", "forged")
    assert client.get("/users/me").status_code == 401
    client.cookies.clear()
    sign_in(client, account)
    from app.db.models.session import UserSession

    with client.sessions() as db:
        session = db.scalar(select(UserSession))
        assert session.token_hash != client.cookies.get("inventory_session")
        session.expires_at = datetime.now(UTC).replace(tzinfo=None) - timedelta(seconds=1)
        db.commit()
    assert client.get("/users/me").status_code == 401


def test_login_rotates_session_and_secure_cookie_can_be_enabled(client, account, monkeypatch):
    sign_in(client, account)
    old_token = client.cookies.get("inventory_session")
    monkeypatch.setenv("SESSION_COOKIE_SECURE", "true")
    response = sign_in(client, account)
    assert "secure" in response.headers["set-cookie"].lower()
    client.cookies.clear()
    client.cookies.set("inventory_session", old_token)
    assert client.get("/users/me").status_code == 401


@pytest.mark.parametrize("path", ["/users/login", "/users/logout"])
def test_cross_origin_session_changes_are_rejected(client, account, path):
    response = client.post(path, json={"username": "kea", "password": account["password"]}, headers={"Origin": "https://attacker.example"})
    assert response.status_code == 403


def test_login_rejects_passwords_beyond_bcrypt_limit(client):
    account = {"username": "limit", "email": "limit@example.com", "first_name": "Kea", "last_name": "Nhlapo", "password": "a" * 72}
    assert client.post("/users/register", json=account).status_code == 201
    response = client.post("/users/login", json={"username": "limit", "password": "a" * 72 + "wrong-suffix"})
    assert response.status_code == 422
    assert client.get("/users/me").status_code == 401
