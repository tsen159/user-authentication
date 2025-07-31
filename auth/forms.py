from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo


class RegistrationForm(FlaskForm):
    """
    Form for user registration.
    Includes fields for username, password, password confirmation, and a submit button.
    """

    username = StringField(
        "Username",
        validators=[
            DataRequired(message="Username is required"),
            Length(
                min=2, max=20, message="Username must be between 2 and 20 characters"
            ),
        ],
    )
    password = StringField(
        "Password",
        validators=[
            DataRequired(message="Password is required"),
            Length(
                min=6, max=20, message="Password must be between 6 and 20 characters!"
            ),
        ],
    )
    confirm_password = StringField(
        "Confirm Password",
        validators=[
            DataRequired(message="Please confirm your password"),
            EqualTo("password", message="Passwords must match!"),
        ],
    )
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    """
    Form for user login.
    Includes fields for username and password, and a submit button.
    """

    username = StringField(
        "Username",
        validators=[DataRequired(message="Username is required")],
    )
    password = StringField(
        "Password",
        validators=[DataRequired(message="Password is required")],
    )
    submit = SubmitField("Login")
