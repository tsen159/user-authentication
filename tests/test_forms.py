import pytest
from auth.forms import RegistrationForm, LoginForm


# test validattion with valid data
def test_registration_form_valid_data(app):
    with app.app_context():
        form = RegistrationForm(
            username="testuser",
            password="testpassword",
            confirm_password="testpassword",
        )
        assert form.validate() is True  # request method does not matter
        assert not form.errors


# test empty username
def test_registration_form_empty_username(app):
    with app.app_context():
        form = RegistrationForm(
            username="",
            password="testpassword",
            confirm_password="testpassword",
        )
        assert form.validate() is False
        assert form.username.errors


# test empty password
def test_registration_form_empty_password(app):
    with app.app_context():
        form = RegistrationForm(
            username="testuser",
            password="",
            confirm_password="testpassword",
        )
        assert form.validate() is False
        assert form.password.errors


# test username length
def test_registration_form_username_length(app):
    with app.app_context():
        form = RegistrationForm(
            username="a",
            password="testpassword",
            confirm_password="testpassword",
        )
        assert form.validate() is False
        assert form.username.errors


# test password length
def test_registration_form_password_length(app):
    with app.app_context():
        form = RegistrationForm(
            username="testuser",
            password="short",
            confirm_password="short",
        )
        assert form.validate() is False
        assert form.password.errors


# test password confirmation
def test_registration_form_password_confirm(app):
    with app.app_context():
        form = RegistrationForm(
            username="testuser",
            password="testpassword",
            confirm_password="differentpassword",
        )
        assert form.validate() is False
        assert form.confirm_password.errors


# test login form with valid data (not considering database existence)
def test_login_form_valid_data(app):
    with app.app_context():
        form = LoginForm(
            username="testuser",
            password="testpassword",
        )
        assert form.validate() is True
        assert not form.errors


# test login form with empty username
def test_login_form_empty_username(app):
    with app.app_context():
        form = LoginForm(
            username="",
            password="testpassword",
        )
        assert form.validate() is False
        assert form.username.errors


# test login form with empty password
def test_login_form_empty_password(app):
    with app.app_context():
        form = LoginForm(
            username="testuser",
            password="",
        )
        assert form.validate() is False
        assert form.password.errors
