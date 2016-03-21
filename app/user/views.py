# -*- coding: UTF-8 -*-

import re

from flask import request, redirect
from flask_restful import Resource
from flask.ext.login import current_user, logout_user, login_user, login_required

from app.user.models import User
from app import login_manager, db
from app.user import api
from app.common.error import ApiError


@login_manager.user_loader
def user_loader(user_id):
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
        return redirect('/')


class Logout(Resource):
    def get(self):
        """Logout the current user."""
        user = current_user
        user.authenticated = False
        db.session.add(user)
        db.session.commit()
        logout_user()
        return redirect('/')


class Register(Resource):
    def post(self):
        user = User(request.form['username'] , request.form['password'])
        db.session.add(user)
        db.session.commit()
        return {"email sent"}


api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')


