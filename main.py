import rest
from flask import Flask
from flask_restful import Api
from data import db_session

app = Flask(__name__)
api = Api(app)

api.add_resource(rest.create_user)


def main():
    db_session.global_init("db/ph.db")
    app.run(host="127.0.0.1", port=4000)


if __name__ == '__main__':
    main()
