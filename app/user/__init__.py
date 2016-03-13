from flask import Blueprint
from flask_restful import Api

user_blueprint = Blueprint('user', __name__, url_prefix='/api/user')
api = Api(user_blueprint)

from . import views




