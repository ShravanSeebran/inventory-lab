import pytest
from app.db.repositories.user_repository import UserRepository


def test_create_user(user_repo: UserRepository):
    user_data = {
        "first_name": "Alice",
        "last_name": "Adams",
        "email": "aliceadams@example.com",
        "username": "alice123",
        "hashed_password": "hashedpw",
    }

    user = user_repo.create_user(user_data)

    assert user.id is not None
    assert user.first_name == user_data["first_name"]
    assert user.last_name == user_data["last_name"]
    assert user.email == user_data["email"]
    assert user.username == user_data["username"]
    assert user.hashed_password == user_data["hashed_password"]


def test_create_user_duplicate_email(user_repo: UserRepository):
    user_data = {
        "first_name": "Bob",
        "last_name": "Brown",
        "email": "bobbrown@example.com",
        "username": "bobby123",
        "hashed_password": "hashedpw",
    }

    user_repo.create_user(user_data)

    with pytest.raises(ValueError) as exc:
        user_repo.create_user({**user_data, "username": "bobby456"})

    assert "User creation failed" in str(exc.value)


def test_get_user_methods(user_repo: UserRepository):
    user_data = {
        "first_name": "Carol",
        "last_name": "Clark",
        "email": "carolclark@example.com",
        "username": "carol123",
        "hashed_password": "hashedpw",
    }
    user = user_repo.create_user(user_data)

    assert user_repo.get_user_by_id(user.id) == user
    assert user_repo.get_user_by_email(user.email) == user
    assert user_repo.get_user_by_username(user.username) == user


def test_update_user(user_repo: UserRepository):
    user_data = {
        "first_name": "Dave",
        "last_name": "Danvers",
        "email": "dave@example.com",
        "username": "daveyreal",
        "hashed_password": "hashedpw",
    }
    user = user_repo.create_user(user_data)

    updated = user_repo.update_user(
        user.id, {"first_name": "David", "email": "david@example.com"}
    )
    assert updated is not None
    assert updated.first_name == "David"
    assert updated.email == "david@example.com"


def test_delete_user(user_repo: UserRepository):
    user_data = {
        "first_name": "Eve",
        "last_name": "Ecclestone",
        "email": "eve@example.com",
        "username": "evestone",
        "hashed_password": "hashedpw",
    }
    user = user_repo.create_user(user_data)

    success = user_repo.delete_user(user.id)
    assert success
    assert user_repo.get_user_by_id(user.id) is None


def test_get_users_pagination(user_repo: UserRepository):
    # Create 5 users
    for i in range(5):
        user_repo.create_user(
            {
                "first_name": f"User{i}",
                "last_name": "Test",
                "email": f"user{i}@example.com",
                "username": f"user{i}",
                "hashed_password": "hashedpw",
            }
        )

    users = user_repo.get_users(skip=1, limit=2)
    assert len(users) == 2
    assert users[0].username == "user1"
    assert users[1].username == "user2"
