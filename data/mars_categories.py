import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqAlchemyBase


class Categories(SqAlchemyBase, SerializerMixin):
    __tablename__ = 'category'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    hazard_category = sqlalchemy.Column(sqlalchemy.Integer, default=1, unique=True)

    association_table = sqlalchemy.Table("categories_to_jobs",
                                         SqAlchemyBase.metadata,
                                         sqlalchemy.Column("jobs", sqlalchemy.Integer,
                                                           sqlalchemy.ForeignKey('jobs.id')),
                                         sqlalchemy.Column("categories", sqlalchemy.Integer,
                                                           sqlalchemy.ForeignKey("category.id"))
                                         )
