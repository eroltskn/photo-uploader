import http
import json
import os

from flask import render_template, redirect, url_for, request, flash
from flask import Blueprint

from source.models.models import UserPhotos, db, UserProfile, User

admin_endpoint = Blueprint('admin', __name__)


@admin_endpoint.route("admin/", methods=['GET', 'POST'])
def admin_users():

    user_info = db.session.query(UserProfile).all()

    return render_template('admin/admin_users.html',
                           user_info=user_info
                           )

@admin_endpoint.route("admin/discover_user/<string:user_id>", methods=['GET'])
def discover_photo_user(user_id):

    user_photos = db.session.query(UserPhotos).filter_by(user_id=int(user_id)).all()
    return render_template('admin/discover_user.html',
                           user_photos=user_photos
                           )
