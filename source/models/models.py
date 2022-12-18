"""Data models."""
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

db = SQLAlchemy()


ACCESS = {
    'user': 1,
    'admin': 2
}

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


class UserPhotos(db.Model):
    """Data model for user profile ."""
    __tablename__ = "user_photos"
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    user_id = db.Column(db.Integer,
                        db.ForeignKey("user.id"),
                        primary_key=False)

    user = db.relationship("User",
                           lazy=True,
                           foreign_keys="UserPhotos.user_id")

    image_path = db.Column(db.Text(),
                           index=False,
                           unique=False,
                           nullable=False)

    filename = db.Column(db.Text(),
                         index=False,
                         unique=False,
                         nullable=False)

    created = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), nullable=False)
    modified = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(),
                         onupdate=db.func.current_timestamp(), nullable=False)

    def __init__(self, user_id, image_path,filename):
        self.user_id = user_id
        self.image_path = image_path
        self.filename = filename


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


class User(UserMixin, db.Model):
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

    is_active = db.Column(db.Boolean(),
                          unique=False,
                          nullable=False,
                          default=True)

    access = db.Column(db.Integer)


    def __init__(self, username, password, access=ACCESS['user']):
        self.username = username
        self.password = password
        self.access = access

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method="sha256")

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return "<User {}>".format(self.username)

    def is_admin(self):
        return self.access == ACCESS['admin']

    def is_user(self):
        return self.access == ACCESS['user']

    def allowed(self, access_level):
        return self.access >= access_level
