import base64

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import flask
import flask_login
from sqlalchemy.sql.expression import select

from .. import login_manager
from ..models import User
from ..database import db_session

bp = Blueprint('auth', __name__, url_prefix='/auth')

def get_user_by_email(email):
    user_list = db_session.execute(select(User).where(User.email == email)).all()

    if len(user_list) == 0:
        return

    return user_list[0][0]

def get_user_by_id(id):
    user_list = db_session.execute(select(User).where(User.id == id)).all()

    if len(user_list) == 0:
        return

    return user_list[0][0]

def email_has_user(email):
    if get_user_by_email(email) is None:
        return False

    return True

@login_manager.user_loader
def user_loader(id):
    return get_user_by_id(id)

@login_manager.request_loader
def load_user_from_request(request):
    # TODO rewrite this function, copied from SO and its pretty bad
    # next, try to login using Basic Auth
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Basic ', '', 1)
        decoded_user = str(base64.b64decode(api_key.encode()), encoding="utf-8")
        email, password = decoded_user.strip().split(':')

        user = get_user_by_email(email)
        if user and user.password == User.hash_password(password, user.salt):
            return user

    # finally, return None if both methods did not login the user
    return None

@bp.route('/login', methods=['POST'])
def login():
    email = flask.request.form['email']
    user = get_user_by_email(email)
    hashed_password = User.hash_password(flask.request.form['password'], user.salt)
    if email_has_user(email) and hashed_password == user.password:
        flask_login.login_user(user)
        return 'test'

    return 'Bad login'

@bp.route('/register', methods=['POST'])
def register():
    email = flask.request.form['email']
    password = flask.request.form['password']
    user = User(email, password)

    if email_has_user(email):
        return 'User already exists', 409

    db_session.add(user)
    db_session.commit()

    return 'User registered!'

@bp.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return "Logged out successfully."

# Example protected route which requires login to request
@bp.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + str(flask_login.current_user.salt)
