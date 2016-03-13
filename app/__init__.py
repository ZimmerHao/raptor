# -*- coding: UTF-8 -*-

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from config import load_config
from logging.config import dictConfig
from app.common.hbase import HbaseClient


db = SQLAlchemy()
login_manager = LoginManager()
hbase_client = HbaseClient()


def create_app():
    app = Flask(__name__)
    app.config.from_object(load_config())

    db.init_app(app)
    register_blueprints(app)
    register_logger(app)
    hbase_client.init_app(app)

    return app


def init_login_manager(app):
    login_manager.init_app(app)


def register_blueprints(app):
    from news import news_blueprint
    app.register_blueprint(news_blueprint, url_prefix='/v1.0')

    from org import org_blueprint
    app.register_blueprint(org_blueprint, url_prefix='/v1.0')

def register_logger(app):
    dictConfig(app.config.get('LOGGING'))






