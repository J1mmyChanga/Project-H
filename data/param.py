import sqlalchemy as sql
from data.db_session import SqlAlchemyBase


class Param(SqlAlchemyBase):
    __tablename__ = "params"

    id = sql.Column(sql.Integer, autoincrement=True, unique=True, primary_key=True)
    name = sql.Column(sql.String)
