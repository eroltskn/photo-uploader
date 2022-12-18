from flask import Blueprint
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user

from source.helpers.forms import SignupForm, LoginForm
from source.models.models import db, User, UserProfile
from . import login_manager

user_endpoint = Blueprint('user', __name__)


@user_endpoint.route("user/login", methods=["GET", "POST"])
def login():
    # Bypass if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for("photo.home_photo"))

    form = LoginForm()
    # Validate login attempt
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(password=form.password.data):
            login_user(user)
            next_page = request.args.get("next")
            return redirect(next_page or url_for("photo.home_photo"))
        flash("Invalid username/password combination")
        return redirect(url_for("photo.photo"))

    return render_template(
        "user/login.html",
        form=form,
        title="Log in.",
        template="login-page",
        body="Log in with your User account.",
    )


@user_endpoint.route("user/register", methods=["GET", "POST"])
def register():
    form = SignupForm()
    try:
        if form.validate_on_submit():
            existing_user = User.query.filter_by(username=form.username.data).first()

            if existing_user is None:
                user = User(
                    username=form.username.data, password=form.password.data
                )
                user.set_password(form.password.data)
                db.session.add(user)
                db.session.flush()
                db.session.refresh(user)
                user_profile = UserProfile(user_id=user.id,
                                           email=form.email.data,
                                           first_name=form.first_name.data,
                                           last_name=form.last_name.data)
                db.session.add(user_profile)

                db.session.commit()  # Create new user
                login_user(user)  # Log in as newly created user
                return redirect(url_for("home.home"))

            flash("A user already exists with that username.")

    except Exception as e:
        db.session.rollback()
        flash("An error occurred.")

    return render_template(
        "user/register.html",
        title="Create an Account.",
        form=form,
        template="signup-page",
        body="Sign up for a user account.",
    )


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash("You must be logged in to view that page.")
    return redirect(url_for("auth_bp.login"))


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in upon page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None

