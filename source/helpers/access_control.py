from flask import flash, redirect, url_for

from flask_login import  current_user
from functools import wraps




### custom wrap to determine access level ###
def requires_access_level(access_level):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated: #the user is not logged in
                return redirect(url_for('login'))

            if not current_user.allowed(access_level):
                flash('You do not have access to this resource.', 'danger')
                return redirect(url_for('home.home'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
