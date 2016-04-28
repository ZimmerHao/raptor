from flask import Blueprint
from flask_restful import Api

tools_blueprint = Blueprint('tools', __name__)
api = Api(tools_blueprint)

from . import views