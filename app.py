"""

For this app to work, two environment variables need to be set:
`PFIN_SERVER`: The endpoint leading to the MongoDB server.
`PFIN_SECRET`: A secret key used by Flask.

"""

import logging

import pfin

from flask import Flask, session, redirect, render_template, url_for, request
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

from functools import wraps


##############
# Flask init #
##############


app = Flask(__name__)

# Get Flask secret
PFIN_SERVER = pfin.config.PFIN_SERVER
PFIN_SECRET = pfin.config.PFIN_SECRET

if PFIN_SECRET == "" or PFIN_SERVER == "":
    raise ValueError('Please set your configuration variables. '
                     'They are needed to run the server.')

app.config['SECRET_KEY'] = PFIN_SECRET.encode()


##################
# Databases init #
##################


image_db = pfin.ImageDatabase('PFIN', 'images')
user_db = pfin.UserDatabase('PFIN', 'users')


###################
# User management #
###################


login_manager = LoginManager()
login_manager.init_app(app)


authenticated_users = {}


@login_manager.user_loader
def load_user(user_identifier):
    if user_identifier in authenticated_users:
        return authenticated_users[user_identifier]


def permissions_required(group_id):
    """
    Decorator used to indicate that an endpoint needs authentication to be accessed.
    Takes care of both checking if the user is logged_in,
    and if it has access to the resource.
    Note on the rights:
    - 0: guest
    - 1: regional
    - 2: national
    """
    mapping = {
        0: 'guest',
        1: 'regional',
        2: 'national'
    }

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = session.get('current_user')
            if user.group == mapping[group_id]:
                return func(*args, **kwargs)
            else:
                result = "Action forbidden ; insufficient rights."
                logging.info(result + f" User id: {user.user_id} ; Function called: {func.__name__}")
                return
        return wrapper
    return decorator


def require_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('current_user') is not None:
            return func(*args, **kwargs)
        else:
            return redirect('/')
    return wrapper


##########
# Webapp #
##########


@app.route('/')
def home():
    return render_template('index.html', image_db=image_db, user=current_user)


@app.route('/sort', methods=['GET', 'POST'])
def sort():
    return render_template('sort.html', user=current_user)


@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    user = user_db.login_user(email, password)
    if user is not None:
        # Logged in successfully.
        login_user(user)
        global authenticated_users
        authenticated_users.update({user.get_id(): user})
        return redirect(url_for('dashboard'))
    else:
        return redirect('/')


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
