import pytest
from auth.models import User


# Test user name
def test_user_creation_valid_data(app):
    with app.app_context():
        user = User(username="validuser")  # type: ignore
        assert user.username == "validuser"


# Test password hashing
def test_user_set_password(app):
    with app.app_context():
        user = User(username="testuser")  # type: ignore
        raw_password = "testpassword"
        user.set_password(raw_password)
        assert user.password is not None  # Password should be hashed and not None
        assert raw_password != user.password  # Ensure password is hashed


# Test password checking
def test_user_check_password(app):
    with app.app_context():
        user = User(username="testuser")  # type: ignore
        raw_password = "testpassword"
        user.set_password(raw_password)

        assert user.check_password(raw_password) is True
        assert user.check_password("wrongpassword") is False
        assert user.check_password("") is False  # Empty password
