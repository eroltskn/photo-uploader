"""Data models."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class UserRole(db.Model):
    """Data model for user role."""

    __tablename__ = "user_role"
    role_id = db.Column(db.Integer,
                        db.ForeignKey("role.id"),
                        primary_key=True)

    user_id = db.Column(db.Integer,
                        db.ForeignKey("user.id"),
                        primary_key=True)

    user = db.relationship("User",
                           backref='user_role',
                           lazy=True
                           )

    roles = db.relationship("Role",
                            backref="user_role",
                            lazy=True,
                            )

    def __init__(self, role_id, user_id):
        self.role_id = role_id
        self.user_id = user_id


class UserProfile(db.Model):
    """Data model for user profile ."""
    __tablename__ = "user_profile"
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    user_id = db.Column(db.Integer,
                        db.ForeignKey("user.id"),
                        primary_key=False)

    user = db.relationship("User",
                           lazy=True,
                           foreign_keys="UserProfile.user_id")

    email = db.Column(db.String(45),
                      index=False,
                      unique=True,
                      nullable=False)

    first_name = db.Column(db.String(45),
                           index=False,
                           unique=False,
                           nullable=False)

    last_name = db.Column(db.String(45),
                          index=False,
                          unique=False,
                          nullable=False)

    created = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), nullable=False)
    modified = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(),
                         onupdate=db.func.current_timestamp(), nullable=False)

    def __init__(self, user_id, email, first_name, last_name):
        self.user_id = user_id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name


class Role(db.Model):
    """Data model for role."""

    __tablename__ = "role"
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    name = db.Column(db.String(45),
                     index=False,
                     unique=True,
                     nullable=False)



class User(db.Model):
    """Data model for user ."""

    __tablename__ = "user"
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    username = db.Column(db.String(45),
                         index=False,
                         unique=True,
                         nullable=False)
    password = db.Column(db.Text(),
                         index=False,
                         unique=False,
                         nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password