from flask import request, session, url_for, redirect, jsonify
from flask.views import MethodView
from werkzeug.exceptions import BadRequest
from utils.views import ViewMixin
from Crypto.Protocol.KDF import bcrypt, bcrypt_check

NAME_PREFIX = 'staff'
ROUTE_PREFIX = '/staff'


def register_views(app):
    IndexView.register_rule(app)
    LoginView.register_rule(app)
    LogoutView.register_rule(app)
    UserView.register_rule(app)
    UserAuthView.register_rule(app)


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
        "email": "firstpotato@gmail.com",
        "password": "12345",
    },
    2: {
        "username": "ally",
        "email": "ally@gmail.com",
        "password": "54321",
    },
}


class UserView(BaseView, MethodView):

    name = 'user'
    route = '/user/<int:user_id>'

    def get(self, user_id=None):
        user = users.get(user_id)
        if not user:
            raise BadRequest
        return jsonify(user)


class UserAuthView(BaseView, MethodView):

    name = 'user_auth'
    route = '/user/auth'

    def get(self):
        username = request.args.get('username')
        email = request.args.get('email')
        password = request.args.get('password')
        if email is None and username is None:
            raise BadRequest
        user_id = None
        if email is not None:
            email = email.strip().lower()
            for id, info in users.items():
                if info['email'].strip().lower() == email:
                    user_id = id
                    break
        else:
            username = username.strip().lower()
            for id, info in users.items():
                if info['username'].strip().lower() == username:
                    user_id = id
                    break
        if user_id is None:
            return jsonify({})
        if info['password'] != password:
            return jsonify({})
        return jsonify(info)

