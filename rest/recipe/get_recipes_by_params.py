import random
from flask import jsonify, request
from flask_restful import Resource

from data import db_session
from data.recipes import Recipe


class GetRecipesByParams(Resource):
    @staticmethod
    def get():
        db_sess = db_session.create_session()

        params = list(map(lambda x: str(x), request.json["params"]))
        all_recipes = db_sess.query(Recipe).all()
        best_recipes = []
        for recipe in all_recipes:
            max_equality = 0
            for param in params:
                if param in recipe.criteria.split(","):
                    max_equality += 1
            if max_equality > len(params) // 2:
                best_recipes.append(recipe)
        a = random.choice(best_recipes)

        return jsonify({
            "id": a.id,
            "name": a.name
        })
