from flask import jsonify, request
from flask_restful import Resource

from data import db_session
from data.recipes import Recipe


class GetRecipeRequest(Resource):
    @staticmethod
    def get():
        db_sess = db_session.create_session()

        recipe_id = request.json["id"]
        recipe = db_sess.query(Recipe).filter(Recipe.id == recipe_id).first()

        return jsonify({
            "id": recipe.id,
            "criteria": map(lambda x: int(x), recipe.criteria.split(",")),
            "cooking": recipe.cooking,
            "products": recipe.products
        })
