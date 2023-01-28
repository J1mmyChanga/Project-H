import rest
from flask import Flask
from flask_restful import Api
from data import db_session

app = Flask(__name__)
api = Api(app)

api.add_resource(rest.CreateUserRequest, "/api/user/create")
api.add_resource(rest.CheckUserPassRequest, "/api/user/check_pass")
api.add_resource(rest.GetUserRequest, "/api/user/get")
api.add_resource(rest.GetLastRecipeRequest, "/api/user/get_last_recipe")
api.add_resource(rest.SetLastRecipeRequest, "/api/user/set_last_recipe")

api.add_resource(rest.GetRecipesByParams, "/api/recipes/get_recipes")
api.add_resource(rest.GetRecipeRequest, "/api/recipes/get_recipe")


def main():
    db_session.global_init("db/ph.db")
    app.run(host="127.0.0.1", port=4000)


if __name__ == '__main__':
    main()
