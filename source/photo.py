import os

from flask import render_template, redirect, url_for, request, flash
from flask import Blueprint
from werkzeug.utils import secure_filename
from flask import current_app as app
from source.helpers.forms import PhotoForm
from flask_login import current_user

from source.models.models import UserPhotos, db

home_photo_endpoint = Blueprint('photo', __name__)


@home_photo_endpoint.route("photo/home")
def home_photo():
    """Landing page route."""
    nav = [
        {"name": "Upload Photo", "url": "/photo/upload"},
        {"name": "Discover Photos", "url": "/photo/discover"},
    ]

    return render_template(
        "photo/photo_home.html",
        nav=nav,
        title="Home Page Photo Uploaderrrr",
        description="Welcome to Landing Page",
    )


@home_photo_endpoint.route("photo/upload", methods=['GET', 'POST'])
def upload_photo():
    image_path =None
    try:
        if request.method == 'POST':
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']

            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(image_path)

                user_profile = UserPhotos(user_id=current_user.get_id(),
                                          image_path=image_path,
                                          filename='assets/img/'+filename)

                db.session.add(user_profile)

                db.session.commit()

                return redirect(url_for('photo.upload_photo', name=filename))
    except Exception as e:
        os.remove(image_path)
        db.session.rollback()
        flash("an error occurred")

    user_photos = UserPhotos.query.filter_by(user_id=current_user.get_id()).all()

    return render_template('photo/upload_photo.html',
                           title='User Form',
                           user_photos=user_photos
                           )


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
