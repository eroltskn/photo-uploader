from flask import render_template
from flask import Blueprint

from source.helpers.access_control import requires_access_level
from source.models.models import UserPhotos, db, UserProfile, User, ACCESS

admin_endpoint = Blueprint('admin', __name__)


@admin_endpoint.route("admin/", methods=['GET', 'POST'])
@requires_access_level(ACCESS['admin'])
def admin_users():

    user_info = db.session.query(UserProfile).all()

    return render_template('admin/admin_users.html',
                           user_info=user_info
                           )

@admin_endpoint.route("admin/discover_user/<string:user_id>", methods=['GET'])
@requires_access_level(ACCESS['admin'])
def discover_photo_user(user_id):

    user_photos = db.session.query(UserPhotos).filter_by(user_id=int(user_id)).all()
    return render_template('admin/discover_user.html',
                           user_photos=user_photos
                           )
