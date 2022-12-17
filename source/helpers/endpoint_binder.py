from flask import current_app

from source.user import user_endpoint
from source.home import home_endpoint

def bind_endpoints():
    current_app.register_blueprint(user_endpoint, url_prefix='/')
    current_app.register_blueprint(home_endpoint, url_prefix='/')
