from flask import jsonify, request
from flask_restful import Resource

from data import db_session
from data.user import User


class GetUserRequest(Resource):
    @staticmethod
    def get():
        db_sess = db_session.create_session()

        user_id = request.json["id"]
        user = db_sess.query(User).filter(User.id == user_id).first()

        return jsonify({
            "id": user.id,
            "name": user.name,
            "phone": user.phone,
            "last_recipe": user.last_recipe.id
        })
