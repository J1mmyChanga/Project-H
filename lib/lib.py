import requests


class Lib:
    server_address = "http://127.0.0.1:5000"
    session = requests.Session()

    @classmethod
    def register(cls, phone, password):
        res = cls.session.post(cls.server_address + "/api/user/create", json={
            "name": '___',
            "phone": phone,
            "password": password
        })
        return res.json()["id"]

    @classmethod
    def check_password(cls, user_id, password): ...

    @classmethod
    def get_user(cls, user_id): ...

    @classmethod
    def get_last_recipe_request(cls, user_id): ...

    @classmethod
    def set_last_recipe_request(cls, user_id, recipe_id): ...
