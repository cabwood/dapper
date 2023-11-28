from flask import request, session, url_for, redirect
from flask.views import MethodView
from werkzeug.exceptions import BadRequest
from utils.views import ViewMixin

NAME_PREFIX = 'staff'
ROUTE_PREFIX = '/staff'

def register_views(app):
    IndexView.register_rule(app)
    LoginView.register_rule(app)
    LogoutView.register_rule(app)
    AuthUser.register_rule(app)


class BaseView(ViewMixin):

    name_prefix = NAME_PREFIX
    route_prefix = ROUTE_PREFIX


class IndexView(BaseView, MethodView):

    name = 'index'
    route = '/'

    def get(self):
        if 'username' in session:
            return f'Logged in as {session["username"]}'
        return 'You are not logged in'


class LoginView(BaseView, MethodView):

    name = 'login'
    route = '/login'

    def get(self):
        return '''
            <form method="post">
                <p><input type=text name=username>
                <p><input type=submit value=Login>
            </form>
        '''

    def post(self):
        session['username'] = request.form['username']
        return redirect(url_for(IndexView.full_name))


class LogoutView(BaseView, MethodView):

    name = 'logout'
    route = '/logout'

    def get(self):
        session.pop('username', None)
        return redirect(url_for(IndexView.full_name))

users = {
    1: {
        "username": "simon",
        "password": "12345",
    },
    2: {
        "username": "ally",
        "password": "54321",
    },
}


class AuthUser(BaseView, MethodView):

    name = 'auth_user'
    route = '/auth_user/<int:user_id>'

    def get(self, user_id=None):
        user = users.get(user_id)
        if not user:
            raise BadRequest
        return user['username']
    