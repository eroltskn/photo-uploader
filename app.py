from flask import Flask
from source.constant import Constant as CONSTANT
from source.models.models import db
from flask_migrate import Migrate

"""Construct the core application."""
app = Flask(__name__, template_folder="source/templates", static_folder="source/static")

app.config['SQLALCHEMY_DATABASE_URI'] = CONSTANT.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = CONSTANT.SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    from source import home

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
