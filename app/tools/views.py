# -*- coding: UTF-8 -*-

from flask import request, jsonify
from flask_restful import Resource
from flask_excel import make_response_from_array

from app.user import api


class UploadOrgsExcel(Resource):
    def post(self):
        return jsonify({"result": request.get_array(field_name='file')})


api.add_resource(UploadOrgsExcel, '/upload/orgs', endpoint='upload')