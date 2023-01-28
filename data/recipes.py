import sqlalchemy as sql
from data.db_session import SqlAlchemyBase


class Recipe(SqlAlchemyBase):
    __tablename__ = "recipes"
    __table_args__ = (
        sql.ForeignKeyConstraint(["id"], ["recipes.id"]),
    )

    id = sql.Column(sql.Integer, autoincrement=True, unique=True, primary_key=True)
    name = sql.Column(sql.String)
    criteria = sql.Column(sql.String)
