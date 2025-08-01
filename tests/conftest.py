import pytest
from app import create_app
from auth.models import db, User


@pytest.fixture
def app():
    """
    Create a Flask application instance for testing.
    """
    test_app = create_app()
    test_app.config["TESTING"] = True
    test_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    test_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    test_app.config["SECRET_KEY"] = "test_secret_key"
    test_app.config["WTF_CSRF_ENABLED"] = False  # Disable CSRF for testing

    with test_app.app_context():
        db.create_all()
        yield test_app
        db.session.remove()  # clean up current session
        db.drop_all()  # drop all tables after tests


@pytest.fixture
def client(app):
    """
    Create a test client for the Flask application.
    This allow us to make HTTP requests to the application without running the server.
    """
    return app.test_client()


@pytest.fixture
def test_user(app):
    """
    Create a test user in the database.
    """
    with app.app_context():
        user = User(username="testuser")  # type: ignore
        user.set_password("testpassword")
        db.session.add(user)
        db.session.commit()
        yield user
        db.session.delete(user)
        db.session.commit()


class AuthActions:
    def __init__(self, client):
        self._client = client

    def login(self, username="testuser", password="testpassword"):
        return self._client.post(
            "/login", data={"username": username, "password": password}
        )

    def logout(self):
        return self._client.get("/logout")


@pytest.fixture
def auth(client):
    return AuthActions(client)
