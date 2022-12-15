from flask import Flask


def create_app():
    """Construct the core application."""
    app = Flask(__name__, template_folder="templates", static_folder="static")

    with app.app_context():
        from . import home

        return app
