from flask import Flask
from source.constant import Constant as CONSTANT
from source.models.models import db
from flask_migrate import Migrate
from flask_login import LoginManager

login_manager = LoginManager()


def create_app():
    """Construct the core application."""
    app = Flask(__name__, template_folder="templates", static_folder="static")

    app.config['SQLALCHEMY_DATABASE_URI'] = CONSTANT.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = CONSTANT.SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['SECRET_KEY'] = 'any secret string'
    from os.path import join, dirname, realpath

    UPLOADS_PATH = join(dirname(realpath(__file__)), 'static/assets/img/')

    app.config['UPLOAD_FOLDER'] = UPLOADS_PATH
    login_manager.init_app(app)

    db.init_app(app)
    migrate = Migrate(app, db)

    from source.helpers.endpoint_binder import bind_endpoints
    from source import user

    with app.app_context():
        bind_endpoints()

    return app
