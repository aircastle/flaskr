from flask import (render_template,
                   redirect,
                   url_for,
                   abort,
                   session,
                   escape,
                   request,
                   flash,
                   g)

from flaskext.login import *
from flaskr.model.user import *
from flaskr.controller.form import *
from flaskr.controller.entry import *
from flaskr import *

login_manager = LoginManager()

class LoginUser(UserMixin):
    def __init__(self, id, name=None):
        self.id = id
        self.name = name
        # self.active = active
    # def is_active(self):
    #     return self.active

class Anonymous(AnonymousUser):
    name = u"Anonymous"

login_manager.anonymous_user = Anonymous
login_manager.login_view = "login"
login_manager.login_message = u"Please log in to access this page."
# login_manager.refresh_view = "reauth"
login_manager.setup_app(app)

@login_manager.user_loader
def load_user(id):
    try:
        userobj = User.get_from_userid(id)
        user = LoginUser(int(id),userobj.name)
        return user
    except:
        return None

@login_manager.unauthorized_handler
def unauthorized():
    error = "unauthorized"
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    error = None

    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        #remember = form.remember.data
        remember = 1
        user = User.get_from_username_password(username, password)
        print "*" * 50
        print user
        print "*" * 50
        if user is not None:
            loginuser = LoginUser(user.id, user.name)
            if login_user(loginuser):
                flash('You were logged in')
                return redirect(url_for('show_entries'))
        error = 'Invalid username or password'
    return render_template('login.html', error=error, form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out')
    return redirect(url_for('show_entries'))
