from flask import jsonify, request
from flask_restful import Resource

from data import db_session
from data.user import User
from data.recipes import Recipe


class SetLastRecipeRequest(Resource):
    @staticmethod
    def get():
        db_sess = db_session.create_session()

        user_id = request.json["id"]
        last_recipe_id = request.json["recipe_id"]["id"]

        recipe = db_sess.query(Recipe).filter(Recipe.id == int(last_recipe_id)).first()
        user = db_sess.query(User).filter(User.id == user_id).first()
        user.last_recipe = recipe
        user.last_recipe_id = int(last_recipe_id)
        db_sess.commit()
