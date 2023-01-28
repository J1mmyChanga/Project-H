import sqlalchemy as sql
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from data.db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = "users"

    id = sql.Column(sql.Integer, autoincrement=True, unique=True, primary_key=True)
    phone = sql.Column(sql.String)
    name = sql.Column(sql.String)
    password = sql.Column(sql.String)

    last_recipe = relationship("Recipe")

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
