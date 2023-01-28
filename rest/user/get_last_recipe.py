from flask import jsonify, request
from flask_restful import Resource

from data import db_session
from data.user import User


class GetLastRecipeRequest(Resource):
    @staticmethod
    def get():
        db_sess = db_session.create_session()

        user_id = request.json["id"]
        user = db_sess.query(User).filter(User.id == user_id).first()
        last_recipe = user.last_recipe

        return jsonify({
            "id": last_recipe.id,
            "name": last_recipe.name,
            "criteria": map(lambda x: int(x), last_recipe.criteria.split(",")),
            "products": last_recipe.products,
            "cooking": last_recipe.cooking
        })
