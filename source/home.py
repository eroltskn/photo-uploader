from flask import render_template
from flask import Blueprint

home_endpoint = Blueprint('', __name__)


@home_endpoint.route("/")
def home():
    """Landing page route."""
    nav = [
        {"name": "Login", "url": "user/login"},
        {"name": "Signup", "url": "user/register"},
    ]
    return render_template(
        "home/home.html",
        nav=nav,
        title="Home Page Photo Uploaderrrr",
        description="Welcome to Landing Page",
    )