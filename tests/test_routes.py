import pytest
from auth.models import User, db


# test / route
def test_home_redirect(client):
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 302  # should redirect
    assert (
        response.location == "/login"
    )  # response.location should point to the targeted redirect URL


# test for /register route
# test whether registration page loads correctly
def test_register_page(client):
    response = client.get("/register")  # mock GET request
    assert response.status_code == 200
    assert b"Register" in response.data or b"Sign up" in response.data
    assert response.request.path == "/register"


# test for registration
def test_register_success(client):
    response = client.post(
        "/register",
        data={
            "username": "testuser",
            "password": "testpassword",
            "confirm_password": "testpassword",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert response.request.path == "/login"
    assert b"Your account has been created!" in response.data

    # check if user is created in the database
    user = User.query.filter_by(username="testuser").first()
    assert user is not None
    assert user.check_password("testpassword")  # verify password hashing


@pytest.mark.parametrize(
    "username, password, confirm_pwd, expected_message",
    [
        ("testuser", "testpassword", "testpassword", "Username already exists."),
        ("newuser", "newpassword", "differentpassword", "Passwords must match!"),
    ],
)
def test_register_failed(
    client, test_user, username, password, confirm_pwd, expected_message
):
    response = client.post(
        "/register",
        data={
            "username": username,
            "password": password,
            "confirm_password": confirm_pwd,
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert expected_message in response.text
    assert response.request.path == "/register"


# test /login route
# test login page
def test_login_page(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert b"Login" in response.data or b"Sign in" in response.data
    assert response.request.path == "/login"


# test login with a existing user
def test_login_success(client, test_user, auth):
    response = auth.login("testuser", "testpassword")
    assert response.status_code == 302  # should redirect to dashboard
    assert response.location == "/dashboard"
    with client.session_transaction() as session:
        assert session["user_id"] == test_user.id


# test non existing user login, wrong password
@pytest.mark.parametrize(
    "username, password",
    [
        ("nonexistent", "wrongpassword"),
        ("testuser", "wrongpassword"),
    ],
)
def test_login_fail(auth, username, password):
    response = auth.login(username, password)
    assert response.status_code == 200
    assert response.request.path == "/login"
    assert b"Login unsuccessful." in response.data


# test /dashboard route
def test_dashboard_login_access(client, auth, test_user):
    auth.login("testuser", "testpassword")
    response = client.get("/dashboard")
    assert response.status_code == 200
    assert response.request.path == "/dashboard"


def test_dashboard_not_logged_in(client):
    response = client.get("/dashboard", follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/login"


# test /logout route
def test_logout(client, auth, test_user):
    auth.login("testuser", "testpassword")
    response = auth.logout()

    assert response.status_code == 302
    assert response.location == "/login"

    with client.session_transaction() as session:
        assert "user_id" not in session
