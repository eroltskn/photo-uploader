from flask import render_template
from flask import Blueprint
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user

from source.helpers.forms import SignupForm
from source.models.models import db, User, UserProfile
from . import login_manager

user_endpoint = Blueprint('user', __name__)

@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in upon page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None


@user_endpoint.route("user/register", methods=["GET", "POST"])
def register():
    """
    User sign-up page.

    GET requests serve sign-up page.
    POST requests validate form & user creation.
    """
    form = SignupForm()
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
            return redirect(url_for("/"))
        flash("A user already exists with that username.")

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
