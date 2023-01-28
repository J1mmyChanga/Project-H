from flask import jsonify, request
from flask_restful import Resource

from data import db_session
from data.user import User


class CheckUserPassRequest(Resource):
    @staticmethod
    def post():
        db_sess = db_session.create_session()

        user_id = request.json["id"]
        password = request.json["password"]

        user = db_sess.query(User).filter(User.id == user_id).first()

        if user.check_password(password):
            return jsonify("correct")
        return jsonify("wrong")
