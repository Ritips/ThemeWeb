import sqlalchemy
from sqlalchemy import orm
from .db_session import SqAlchemyBase


class Jobs(SqAlchemyBase):
    __tablename__ = 'jobs'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    team_leader = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    job = sqlalchemy.Column(sqlalchemy.String)
    work_size = sqlalchemy.Column(sqlalchemy.Integer)
    collaborators = sqlalchemy.Column(sqlalchemy.String)
    start_date = sqlalchemy.Column(sqlalchemy.DateTime)
    end_date = sqlalchemy.Column(sqlalchemy.DateTime)
    is_finished = sqlalchemy.Column(sqlalchemy.Boolean)

    user = orm.relationship('User')

    def __repr__(self):
        return f'<Job> {self.job}'

    def set_information(self, team_leader, job, work_size, collaborators, start_date, end_date, is_finished):
        self.team_leader, self.job, self.work_size, self.collaborators = team_leader, job, work_size, collaborators
        self.start_date, self.end_date, self.is_finished = start_date, end_date, is_finished
