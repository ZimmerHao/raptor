# -*- coding: UTF-8 -*-

import datetime

from app import db


class User(db.Model):
    __table_args__ = {"schema": "haojm"}
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    mobile = db.Column(db.String(120), unique=True, nullable=True)
    password = db.Column(db.String(80))
    authenticated = db.Column(db.Boolean, default=False)
    date_joined = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)

    def __init__(self, username=None, email=None, mobile=None, password=None, authenticated=True,
                 date_joined=None, is_active=True):
        self.username = username
        self.email = email
        self.mobile = mobile
        self.password = password
        self.authenticated = authenticated
        if not date_joined:
            self.date_joined = datetime.datetime.now()
        self.is_active = is_active

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return self.is_active

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % self.username
