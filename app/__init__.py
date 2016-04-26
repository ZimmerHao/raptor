# -*- coding: UTF-8 -*-

from flask import Flask, session
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, current_user
from config import load_config
from logging.config import dictConfig
from app.common.hbase import HbaseClient
from app.common.session import BeakerSessionInterface
from beaker.middleware import SessionMiddleware
from flask.ext.principal import Principal, identity_loaded, UserNeed, RoleNeed


db = SQLAlchemy()
login_manager = LoginManager()
hbase_client = HbaseClient()


def create_app():
    app = Flask(__name__)
    app.config.from_object(load_config())

    Principal(app)
    init_load_identity(app)
    db.init_app(app)
    register_blueprints(app)
    register_logger(app)
    hbase_client.init_app(app)
    init_session(app)
    init_login_manager(app)

    return app


def init_login_manager(app):
    login_manager.init_app(app)


def register_blueprints(app):
    from user import user_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/v1.0')

    from news import news_blueprint
    app.register_blueprint(news_blueprint, url_prefix='/v1.0')

    from org import org_blueprint
    app.register_blueprint(org_blueprint, url_prefix='/v1.0')


def register_logger(app):
    dictConfig(app.config.get('LOGGING'))


def init_session(app):
    app.wsgi_app = SessionMiddleware(app.wsgi_app, app.config.get('SESSION_OPTS'))
    app.session_interface = BeakerSessionInterface()


def init_load_identity(app):
    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        # Set the identity user object
        identity.user = current_user

        # Add the UserNeed to the identity
        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))

        # Assuming the User model has a list of roles, update the
        # identity with the roles that the user provides
        if hasattr(current_user, 'roles'):
            for role in current_user.roles:
                identity.provides.add(RoleNeed(role.name))





