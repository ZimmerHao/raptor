# -*- coding: UTF-8 -*-

import re

from flask import request, redirect, current_app, session
from flask_restful import Resource
from flask.ext.login import current_user, logout_user, login_user, login_required
from flask.ext.principal import identity_changed, Identity, RoleNeed, UserNeed, AnonymousIdentity

from app.user.models import User
from app import login_manager, db
from app.user import api
from app.common.error import ApiError


@login_manager.user_loader
def load_user(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve
    """
    return User.query.get(user_id)


@login_manager.request_loader
def request_loader(request):
    pass


class Login(Resource):
    def post(self):
        user = request.form.get('user', '')
        password = request.form.get('password', '')
        p = re.compile(r'^[\d]{11}$')
        if re.match(p, user):
            u = User.query.filter(User.mobile == int(user), User.password == password).first()
        else:
            u = User.query.filter(User.email == user, User.password == password).first()

        if not u:
            return ApiError(40001)
        login_user(u)
        # Tell Flask-Principal the identity changed
        identity_changed.send(current_app._get_current_object(),
                              identity=Identity(u.id))
        return redirect('/')


class Logout(Resource):
    def get(self):
        """Logout the current user."""
        user = current_user
        user.authenticated = False
        db.session.add(user)
        db.session.commit()
        logout_user()
        identity_changed.send(current_app._get_current_object(),
                              identity=AnonymousIdentity())
        return redirect('/')


class Register(Resource):
    def post(self):
        username = request.form.get('username', '')
        email = request.form.get('email', '')
        password = request.form.get('password', '')

        if not (username and email and password):
            return ApiError(40001)
        u = User(username=username, email=email, password=password)
        db.session.add(u)
        db.session.commit()
        identity_changed.send(current_app._get_current_object(),
                              identity=Identity(u.id))

        return redirect('/')


api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(Register, '/join', endpoint='join')


