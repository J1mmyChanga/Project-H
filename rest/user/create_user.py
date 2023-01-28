from flask import jsonify, request
from flask_restful import Resource

from data import db_session
from data.user import User


class CreateUserRequest(Resource):
    @staticmethod
    def post():
        db_sess = db_session.create_session()

        name = request.json["name"]
        phone = request.json["phone"]
        password = request.json["password"]

        user = User()
        user.name = name
        user.phone = phone
        user.set_password(password)
        db_sess.add(user)
        db_sess.commit()

        return jsonify({"id": user.id})
