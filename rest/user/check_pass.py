from flask import jsonify, request
from flask_restful import Resource

from data import db_session
from data.user import User


class CheckUserPassRequest(Resource):
    pass
