import rest
from flask import Flask
from flask_restful import Api
from data import db_session
from data.param import Param

app = Flask(__name__)
api = Api(app)

api.add_resource(rest.CreateUserRequest, "/api/user/create")
api.add_resource(rest.CheckUserPassRequest, "/api/user/check_pass")
api.add_resource(rest.GetUserRequest, "/api/user/get")


def main():
    db_session.global_init("db/ph.db")
    db_sess = db_session.create_session()
    param = Param()
    param.name = "Кино"
    db_sess.add(param)
    db_sess.commit()
    app.run(host="127.0.0.1", port=4000)


if __name__ == '__main__':
    main()
