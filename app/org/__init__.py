from flask import Blueprint
from flask_restful import Api

org_blueprint = Blueprint('org', __name__)
api = Api(org_blueprint)

from . import views




