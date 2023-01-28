from flask import jsonify, request
from flask_restful import Resource

from data.user import User


class CreateUserRequest(Resource):
    @staticmethod
    def post():
        name = request.json["name"]
        phone = request.json["phone"]
        password = request.json["password"]

        user = User()
        user.name = name
        user.phone = phone
        user.set_password(password)

        return jsonify("successful")
