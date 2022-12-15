"""Route declaration."""
from flask import current_app as app
from flask import render_template


@app.route("/")
def home():
    """Landing page route."""
    nav = [
        {"name": "Login", "url": "https://example.com/1"},
        {"name": "Signup", "url": "https://example.com/2"},
    ]
    return render_template(
        "home.html",
        nav=nav,
        title="Home Page Photo Uploader",
        description="Welcome to Landing Page",
    )