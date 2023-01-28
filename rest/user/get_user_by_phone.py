from flask import jsonify, request
from flask_restful import Resource

from data import db_session
from data.user import User


class GetUserByPhone(Resource):
    @staticmethod
    def get():
        phone = request.json["phone"]
        db_sess = db_session.create_session()

        user = db_sess.query(User).filter(User.phone == phone).first()
        return jsonify({"id": user.id})
