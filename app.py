"""

For this app to work, two environment variables need to be set:
`PFIN_SERVER`: The endpoint leading to the MongoDB server.
`PFIN_SECRET`: A secret key used by Flask.

"""

import os

import pfin

import flask
import flask_login


##############
# Flask init #
##############


app = flask.Flask(__name__)

# Get Flask secret
PFIN_SERVER = pfin.config.PFIN_SERVER
PFIN_SECRET = pfin.config.PFIN_SECRET

if PFIN_SECRET == "" or PFIN_SERVER == "":
    raise ValueError('Please set your configuration variables. '
                     'They are needed to run the server.')

# app.secret_key(PFIN_SECRET)


##################
# Databases init #
##################


image_db = pfin.ImageDatabase('PFIN', 'images')
user_db = pfin.UserDatabase('PFIN', 'users')


###################
# User management #
###################


login_manager = flask_login.LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def user_loader(identifier: str):
    """
    :param str identifier: The user's ID (an email address).
    :return User|None:
    """
    if not user_db.does_user_exist(identifier):
        return
    else:
        user = pfin.DummyUser()
        user.id = identifier
        return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    password = request.form.get('password')
    user = user_db.login_user(email, password)
    if user is None:
        return

    user.id = email
    user.is_anonymous = False
    user.is_authenticated = True

    return user


##########
# Webapp #
##########


@app.route('/')
def home():
    return flask.render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'/>
                <input type='password' name='password' id='password' placeholder='password'/>
                <input type='submit' name='submit'/>
               </form>
               '''

    email = flask.request.form.get('email')
    password = flask.request.form.get('password')

    user = user_db.login_user(email, password)
    if user is not None:
        user.id = email
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('dashboard'))
    else:
        return 'Bad login'


@app.route('/dashboard')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'


@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'


if __name__ == '__main__':
    app.run(debug=True)
