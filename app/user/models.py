# -*- coding: UTF-8 -*-

from app import db


class User(db.Model):
    __table_args__ = {"schema": "haojm"}
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    mobile = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(80))

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % self.username
