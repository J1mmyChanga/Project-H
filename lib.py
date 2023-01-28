import requests


class Lib:
    server_address = "http://127.0.0.1:4000"
    session = requests.Session()

    @classmethod
    def register(cls, phone, password):
        res = cls.session.post(cls.server_address + "/api/user/create", json={
            "name": '___',
            "phone": phone,
            "password": password
        }).json()
        return res["id"]

    @classmethod
    def get_user_by_phone(cls, phone):
        res = cls.session.get(cls.server_address + "/api/user/by_phone", json={
            "phone": phone
        }).json()
        return res["id"]

    @classmethod
    def check_password(cls, phone, password):
        res = cls.session.post(cls.server_address + "/api/user/check_pass", json={
            "phone": phone,
            "password": password
        }).json()
        return res == "correct"

    @classmethod
    def get_user(cls, user_id):
        return cls.session.get(cls.server_address + "/api/user/get", json={
            "id": user_id
        }).json()

    @classmethod
    def get_last_recipe_request(cls, user_id):
        return cls.session.get(cls.server_address + "/api/user/get_last_recipe", json={
            "id": user_id
        }).json()

    @classmethod
    def set_last_recipe_request(cls, user_id, recipe_id):
        cls.session.get(cls.server_address + "/api/user/set_last_recipe", json={
            "id": user_id,
            "recipe_id": recipe_id
        })

    @classmethod
    def get_recipe(cls, *params):
        return cls.session.get(cls.server_address + "/api/recipes/get_recipes", json={
            "params": list(params)
        }).json()
