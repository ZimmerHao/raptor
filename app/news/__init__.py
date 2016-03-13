from flask import Blueprint
from flask_restful import Api

news_blueprint = Blueprint('news', __name__)
api = Api(news_blueprint)

from . import views
