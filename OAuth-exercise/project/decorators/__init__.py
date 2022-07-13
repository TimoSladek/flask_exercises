from functools import wraps
from flask import redirect, url_for, session, flash
from flask_login import current_user


def prevent_login_signup(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated:
            flash('You are already logged in!')
            return redirect(url_for('users.index'))
        return fn(*args, **kwargs)

    return wrapper


def ensure_correct_user(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = kwargs.get('user_id') or kwargs.get('id')
        if user_id != current_user.id:
            flash('Not Authorized')
            return redirect(url_for('users.index'))
        return fn(*args, **kwargs)

    return wrapper
