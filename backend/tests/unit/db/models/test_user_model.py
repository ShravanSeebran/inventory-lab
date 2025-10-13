from app.db.models.user import User


def test_user_model_creation():
    user = User(
        email="test@example.com",
        username="testuser",
        first_name="Test",
        last_name="User",
        hashed_password="hashedpassword",
    )
    assert user.email == "test@example.com"
    assert user.username == "testuser"
    assert user.first_name == "Test"
    assert user.last_name == "User"
