from flask import Blueprint
from flask_restful import Api

user_blueprint = Blueprint('user', __name__)
api = Api(user_blueprint)

from . import views




