# -*- coding: UTF-8 -*-

from flask_restful import Resource
from app.user import api
from app.common.logger import logger_flask


class HelloWorld(Resource):
    def get(self):
        logger_flask.info("user ^--^")
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/hello')



