from flask import render_template, session, redirect, url_for, Blueprint, flash
from auth.forms import RegistrationForm, LoginForm
from .models import User, db


bp = Blueprint("auth", __name__)


@bp.route("/")
def home():
    return redirect(url_for("auth.login"))


@bp.route("/register", methods=["GET", "POST"])
def register():
    """
    Route for user registration.
    """
    form = RegistrationForm()
    if form.validate_on_submit():  # automatic validation of form data
        # check if username already exists
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash("Username already exists. Please choose a different one.", "danger")
            return redirect(url_for("auth.register"))

        new_user = User(username=form.username.data)  # type: ignore
        new_user.set_password(form.password.data)  # hash the password
        db.session.add(new_user)
        db.session.commit()
        flash("Your account has been created!", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html", form=form)


@bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Route for user login.
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            session["user_id"] = user.id  # store user ID in session
            return redirect(url_for("auth.dashboard"))
        else:
            flash(
                "Login Unsuccessful. Please check your username or password.", "danger"
            )
    return render_template("login.html", form=form)


@bp.route("/logout")
def logout():
    """
    Route for user logout.
    """
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))


@bp.route("/dashboard")
def dashboard():
    """
    Displays the user's dashboard after successful login.
    """
    if "user_id" not in session:
        flash("You need to log in first.", "warning")
        return redirect(url_for("auth.login"))
    user = User.query.get(session["user_id"])
    return render_template("dashboard.html", username=user.username)  # type: ignore
